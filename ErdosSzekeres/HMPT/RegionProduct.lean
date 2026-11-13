import ErdosSzekeres.HMPT.ChainCapacity
import ErdosSzekeres.HMPT.AntichainCapacity
import ErdosSzekeres.Counting

namespace ErdosSzekeres.HMPT

open Suk
open scoped BigOperators

/-- Actual extremal witnesses in a support region, retaining both cap budgets. -/
structure RegionCapacities (F : CapFrame) (s : Finset Point) where
  chain : SpikeChain F
  antichain : Finset Point
  chain_subset : chain.points ⊆ s
  antichain_subset : antichain ⊆ s
  incomparable : SpikeAntichain F antichain
  chain_max : ∀ D : SpikeChain F, D.points ⊆ s → D.length ≤ chain.length
  antichain_max : ∀ U ⊆ s, SpikeAntichain F U → U.card ≤ antichain.card
  size_le : s.card ≤ chain.length * antichain.card
  vertical : ChainCapacities chain
  horizontal : AntichainCapacity F antichain

theorem exists_regionCapacities (F : CapFrame) (s : Finset Point)
    (hspike : ∀ p ∈ s, p ∈ F.spike) : Nonempty (RegionCapacities F s) := by
  obtain ⟨C, T, hC, hT, ha, hCmax, hTmax, hsize⟩ := exists_max_chain_antichain F s hspike
  obtain ⟨B⟩ := exists_chainCapacities C
  obtain ⟨E⟩ := exists_antichainCapacity F T
  exact ⟨⟨C, T, hC, hT, ha, hCmax, hTmax, hsize, B, E⟩⟩

def RegionCapacities.verticalBudget {F : CapFrame} {s : Finset Point}
    (R : RegionCapacities F s) : ℕ :=
  (max 2 R.vertical.left - 1) + (max 2 R.vertical.right - 1)

def RegionCapacities.horizontalBudget {F : CapFrame} {s : Finset Point}
    (R : RegionCapacities F s) : ℕ := max 2 R.horizontal.cap.card - 1

/-- The finite HMPT part-size estimate in real geometry. The maxima, triangle
order, and supporting caps are constructed rather than assumed numerical data. -/
theorem RegionCapacities.card_le_pow_mul_choose {F : CapFrame} {s P : Finset Point}
    (R : RegionCapacities F s) (hx : F.Horizontal) {n : ℕ} (hn : 3 ≤ n)
    (hgp : GeneralPosition P) (hb : F.b ∈ P) (hc : F.c ∈ P)
    (hs : s ⊆ P) (hspike : ∀ p ∈ s, p ∈ F.spike) (havoid : ¬ HasConvexNGon n P) :
    s.card ≤ 2 ^ R.verticalBudget *
      (R.horizontalBudget + (n - 2)).choose R.horizontalBudget := by
  have hC := R.vertical.length_le_binomial (hgp.mono
    (Finset.insert_subset_iff.mpr ⟨hb, Finset.insert_subset_iff.mpr
      ⟨hc, R.chain_subset.trans hs⟩⟩))
  have hT := R.horizontal.card_le_binomial hx hn
    (hgp.mono (R.antichain_subset.trans hs))
    (fun p hp => hspike p (R.antichain_subset hp)) R.incomparable
    (fun h => havoid (h.mono (R.antichain_subset.trans hs)))
  have hT' : R.antichain.card ≤
      (R.horizontalBudget + (n - 2)).choose R.horizontalBudget := by
    rw [Nat.choose_symm_add]
    have he : R.horizontalBudget + (n - 2) = n + max 2 R.horizontal.cap.card - 3 := by
      unfold RegionCapacities.horizontalBudget
      omega
    rwa [he]
  exact R.size_le.trans (Nat.mul_le_mul
    (hC.trans (Nat.choose_le_two_pow _ _)) hT')

/-- Multiply the geometric region estimates and compress the horizontal
binomials with the proven even/odd budget. The remaining vertical sum is
explicit, for combination with the adjacent-cap budget. -/
theorem region_product_le {r n : ℕ} {P : Finset Point}
    (A : ClockwiseAnchors (r + 3)) (hx : StrictMono (fun i => A.point i 0))
    (Q : Fin r → Finset Point) (R : (i : Fin r) → RegionCapacities (A.frame i) (Q i))
    (hn : 3 ≤ n) (hgp : GeneralPosition P) (hanchors : ∀ i, A.point i ∈ P)
    (hpoints : ∀ i, Q i ⊆ P) (hspike : ∀ i, ∀ p ∈ Q i, p ∈ (A.frame i).spike)
    (havoid : ¬ HasConvexNGon n P) :
    (∏ i, (Q i).card) ≤ 2 ^ (∑ i, (R i).verticalBudget) *
      (2 * (n - 1) + r + r * (n - 2)).choose (2 * (n - 1) + r) := by
  have hcap := parity_cap_budget A (fun i => (R i).antichain)
    (fun i => (R i).horizontal)
    (fun i p hp => hspike i p ((R i).antichain_subset hp))
    (fun i => (R i).incomparable)
    (fun i => (R i).antichain_subset.trans (hpoints i)) havoid
  have hbudget : (∑ i, (R i).horizontalBudget) ≤ 2 * (n - 1) + r := by
    calc
      _ ≤ ∑ i, ((R i).horizontal.cap.card + 1) := by
        apply Finset.sum_le_sum
        intro i _
        unfold RegionCapacities.horizontalBudget
        omega
      _ = (∑ i, (R i).horizontal.cap.card) + r := by simp [Finset.sum_add_distrib]
      _ ≤ 2 * (n - 1) + r := Nat.add_le_add_right hcap r
  have hprod : (∏ i, (Q i).card) ≤
      ∏ i, (2 ^ (R i).verticalBudget *
        ((R i).horizontalBudget + (n - 2)).choose (R i).horizontalBudget) := by
    apply Finset.prod_le_prod'
    intro i _
    exact (R i).card_le_pow_mul_choose (A.frame_horizontal hx i) hn hgp
      (hanchors _) (hanchors _) (hpoints i) (hspike i) havoid
  rw [Finset.prod_mul_distrib, Finset.prod_pow_eq_pow_sum] at hprod
  exact hprod.trans (Nat.mul_le_mul_left _ (by
    simpa using Counting.horizontal_product_le Finset.univ
      (fun i => (R i).horizontalBudget) (n - 2) (2 * (n - 1) + r) hbudget))

/-- The vertical exponent follows from adjacent gluing. Because the support
sequence is a path rather than a cycle, both endpoint capacities are retained.
The additional `2*r` accounts explicitly for padding small capacities to two. -/
theorem vertical_budget_le {r n : ℕ} {P : Finset Point}
    (A : ClockwiseAnchors (r + 3))
    (Q : Fin r → Finset Point) (R : (i : Fin r) → RegionCapacities (A.frame i) (Q i))
    (hn : 4 ≤ n) (hgp : GeneralPosition P) (hanchors : ∀ i, A.point i ∈ P)
    (hpoints : ∀ i, Q i ⊆ P) (havoid : ¬ HasConvexNGon n P) :
    (∑ i, (R i).verticalBudget) ≤ (r + 1) * (n - 1) + 2 * r := by
  have hleft (i) : (R i).vertical.left ≤ n - 1 := by
    have := (R i).vertical.left_lt (fun h =>
      havoid (h.mono ((R i).chain_subset.trans (hpoints i))))
    omega
  have hright (i) : (R i).vertical.right ≤ n - 1 := by
    have := (R i).vertical.right_lt (fun h =>
      havoid (h.mono ((R i).chain_subset.trans (hpoints i))))
    omega
  have hsum : (∑ i, ((R i).vertical.left + (R i).vertical.right)) ≤ (r + 1) * (n - 1) := by
    cases r with
    | zero => simp
    | succ k =>
      have hadj (i : Fin k) :
          (R i.castSucc).vertical.left + (R i.succ).vertical.right ≤ n - 1 := by
        have hlt : (R i.castSucc).vertical.left + (R i.succ).vertical.right < n := by
          by_contra! hsize
          exact havoid (glue_neighboring_chain_caps (R i.castSucc).chain (R i.succ).chain
            (A.adjacent_frames i.val (by omega)) hgp (hanchors _)
            ((R i.castSucc).chain_subset.trans (hpoints _))
            ((R i.succ).chain_subset.trans (hpoints _)) hn hsize
            (R i.castSucc).vertical.left_cap (R i.succ).vertical.right_cap)
        omega
      have hadd := Finset.sum_le_sum (s := Finset.univ) (fun i _ => hadj i)
      simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, smul_eq_mul] at hadd
      have heq : (∑ i : Fin (k + 1), ((R i).vertical.left + (R i).vertical.right)) =
          (∑ i : Fin k, ((R i.castSucc).vertical.left + (R i.succ).vertical.right)) +
            (R (Fin.last k)).vertical.left + (R 0).vertical.right := by
        rw [Finset.sum_add_distrib,
          Fin.sum_univ_castSucc (fun i => (R i).vertical.left),
          Fin.sum_univ_succ (fun i => (R i).vertical.right), Finset.sum_add_distrib]
        omega
      rw [heq]
      have hlast := hleft (Fin.last k)
      have hfirst := hright 0
      nlinarith
  calc
    _ ≤ ∑ i, ((R i).vertical.left + (R i).vertical.right + 2) := by
      apply Finset.sum_le_sum
      intro i _
      unfold RegionCapacities.verticalBudget
      omega
    _ = (∑ i, ((R i).vertical.left + (R i).vertical.right)) + 2 * r := by
      simp [Finset.sum_add_distrib, Nat.mul_comm]
    _ ≤ (r + 1) * (n - 1) + 2 * r := Nat.add_le_add_right hsum _

/-- An explicit support-path bound including endpoint and small-cap losses. -/
def supportProductBound (r n : ℕ) : ℕ :=
  2 ^ ((r + 1) * (n - 1) + 2 * r) *
    (2 * (n - 1) + r + r * (n - 2)).choose (2 * (n - 1) + r)

/-- A complete finite geometric product bound for a horizontal support path.
No chain-size, cap-size, or parity-budget hypothesis remains. -/
theorem support_product_bound {r n : ℕ} {P : Finset Point}
    (A : ClockwiseAnchors (r + 3)) (hx : StrictMono (fun i => A.point i 0))
    (Q : Fin r → Finset Point) (hn : 4 ≤ n)
    (hgp : GeneralPosition P) (hanchors : ∀ i, A.point i ∈ P)
    (hpoints : ∀ i, Q i ⊆ P) (hspike : ∀ i, ∀ p ∈ Q i, p ∈ (A.frame i).spike)
    (havoid : ¬ HasConvexNGon n P) :
    (∏ i, (Q i).card) ≤ supportProductBound r n := by
  let R := fun i => Classical.choice (exists_regionCapacities (A.frame i) (Q i) (hspike i))
  exact (region_product_le A hx Q R (by omega) hgp hanchors hpoints hspike havoid).trans
    (Nat.mul_le_mul_right _ (Nat.pow_le_pow_right (by decide)
      (vertical_budget_le A Q R hn hgp hanchors hpoints havoid)))

end ErdosSzekeres.HMPT
