-- FV302 (24 Nov 2026): the bridge from the compact check over fcatZZs16 to ExcludesHoleBudgetZZsN 16. Generated.
import CompactChecker.Path
import CompactChecker.FcatZZs16
import CompactChecker.Bridge311Bal
import LemmaZ
import LemmaZStar
import BalancedBudgetsZZsN

open ErdosSzekeres.OmissionCertificates
open scoped BigOperators

namespace CompactChecker.BridgeZZs16

theorem node_get_even {l r : FCat} {k : ℕ} (h : k % 2 = 0) : (FCat.node l r).get k = l.get (k / 2) := by
  show (bif Nat.beq (k % 2) 0 then l.get (k / 2) else r.get (k / 2)) = l.get (k / 2)
  rw [h]; rfl

theorem node_get_odd {l r : FCat} {k : ℕ} (h : k % 2 = 1) : (FCat.node l r).get k = r.get (k / 2) := by
  show (bif Nat.beq (k % 2) 0 then l.get (k / 2) else r.get (k / 2)) = r.get (k / 2)
  rw [h]; rfl

theorem eq_3131_11 : ∀ k, k < 2 → k ≠ 1 → fcatZZs16_n11011100001.get k = fcat62_r1083.get k := by
  intro k hk hne
  obtain rfl : k = 0 := by omega
  rfl

theorem eq_3131_10 : ∀ k, k < 4 → k ≠ 3 → fcatZZs16_n1101110000.get k = fcat62_n1101110000.get k := by
  intro k hk hne
  show (FCat.node fcat62_n11011100000 fcatZZs16_n11011100001).get k = (FCat.node fcat62_n11011100000 fcat62_r1083).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq_3131_11 (k / 2) (by omega) (by omega)

theorem eq_3131_9 : ∀ k, k < 8 → k ≠ 6 → fcatZZs16_n110111000.get k = fcat62_n110111000.get k := by
  intro k hk hne
  show (FCat.node fcatZZs16_n1101110000 fcat62_n1101110001).get k = (FCat.node fcat62_n1101110000 fcat62_n1101110001).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq_3131_10 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq_3131_8 : ∀ k, k < 16 → k ≠ 12 → fcatZZs16_n11011100.get k = fcat62_n11011100.get k := by
  intro k hk hne
  show (FCat.node fcatZZs16_n110111000 fcat62_n110111001).get k = (FCat.node fcat62_n110111000 fcat62_n110111001).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq_3131_9 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq_3131_7 : ∀ k, k < 32 → k ≠ 24 → fcatZZs16_n1101110.get k = fcat62_n1101110.get k := by
  intro k hk hne
  show (FCat.node fcatZZs16_n11011100 fcat62_n11011101).get k = (FCat.node fcat62_n11011100 fcat62_n11011101).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq_3131_8 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq_3131_6 : ∀ k, k < 64 → k ≠ 48 → fcatZZs16_n110111.get k = fcat62_n110111.get k := by
  intro k hk hne
  show (FCat.node fcatZZs16_n1101110 fcat62_n1101111).get k = (FCat.node fcat62_n1101110 fcat62_n1101111).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq_3131_7 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq_3131_5 : ∀ k, k < 128 → k ≠ 97 → fcatZZs16_n11011.get k = fcat62_n11011.get k := by
  intro k hk hne
  show (FCat.node fcat62_n110110 fcatZZs16_n110111).get k = (FCat.node fcat62_n110110 fcat62_n110111).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq_3131_6 (k / 2) (by omega) (by omega)

theorem eq_3131_4 : ∀ k, k < 256 → k ≠ 195 → fcatZZs16_n1101.get k = fcat62_n1101.get k := by
  intro k hk hne
  show (FCat.node fcat62_n11010 fcatZZs16_n11011).get k = (FCat.node fcat62_n11010 fcat62_n11011).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq_3131_5 (k / 2) (by omega) (by omega)

theorem eq_3131_3 : ∀ k, k < 512 → k ≠ 391 → fcatZZs16_n110.get k = fcat62_n110.get k := by
  intro k hk hne
  show (FCat.node fcat62_n1100 fcatZZs16_n1101).get k = (FCat.node fcat62_n1100 fcat62_n1101).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq_3131_4 (k / 2) (by omega) (by omega)

theorem eq_3131_2 : ∀ k, k < 1024 → k ≠ 782 → fcatZZs16_n11.get k = fcat62_n11.get k := by
  intro k hk hne
  show (FCat.node fcatZZs16_n110 fcat62_n111).get k = (FCat.node fcat62_n110 fcat62_n111).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq_3131_3 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq_3131_1 : ∀ k, k < 2048 → k ≠ 1565 → fcatZZs16_n1.get k = fcat62_n1.get k := by
  intro k hk hne
  show (FCat.node fcat62_n10 fcatZZs16_n11).get k = (FCat.node fcat62_n10 fcat62_n11).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq_3131_2 (k / 2) (by omega) (by omega)

theorem eq_3132_11 : ∀ k, k < 2 → k ≠ 1 → fcatZZs16_n00111100001.get k = fcat62_r1084.get k := by
  intro k hk hne
  obtain rfl : k = 0 := by omega
  rfl

theorem eq_3132_10 : ∀ k, k < 4 → k ≠ 3 → fcatZZs16_n0011110000.get k = fcat62_n0011110000.get k := by
  intro k hk hne
  show (FCat.node fcat62_n00111100000 fcatZZs16_n00111100001).get k = (FCat.node fcat62_n00111100000 fcat62_r1084).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq_3132_11 (k / 2) (by omega) (by omega)

theorem eq_3132_9 : ∀ k, k < 8 → k ≠ 6 → fcatZZs16_n001111000.get k = fcat62_n001111000.get k := by
  intro k hk hne
  show (FCat.node fcatZZs16_n0011110000 fcat62_n0011110001).get k = (FCat.node fcat62_n0011110000 fcat62_n0011110001).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq_3132_10 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq_3132_8 : ∀ k, k < 16 → k ≠ 12 → fcatZZs16_n00111100.get k = fcat62_n00111100.get k := by
  intro k hk hne
  show (FCat.node fcatZZs16_n001111000 fcat62_n001111001).get k = (FCat.node fcat62_n001111000 fcat62_n001111001).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq_3132_9 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq_3132_7 : ∀ k, k < 32 → k ≠ 24 → fcatZZs16_n0011110.get k = fcat62_n0011110.get k := by
  intro k hk hne
  show (FCat.node fcatZZs16_n00111100 fcat62_n00111101).get k = (FCat.node fcat62_n00111100 fcat62_n00111101).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq_3132_8 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq_3132_6 : ∀ k, k < 64 → k ≠ 48 → fcatZZs16_n001111.get k = fcat62_n001111.get k := by
  intro k hk hne
  show (FCat.node fcatZZs16_n0011110 fcat62_n0011111).get k = (FCat.node fcat62_n0011110 fcat62_n0011111).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq_3132_7 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq_3132_5 : ∀ k, k < 128 → k ≠ 97 → fcatZZs16_n00111.get k = fcat62_n00111.get k := by
  intro k hk hne
  show (FCat.node fcat62_n001110 fcatZZs16_n001111).get k = (FCat.node fcat62_n001110 fcat62_n001111).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq_3132_6 (k / 2) (by omega) (by omega)

theorem eq_3132_4 : ∀ k, k < 256 → k ≠ 195 → fcatZZs16_n0011.get k = fcat62_n0011.get k := by
  intro k hk hne
  show (FCat.node fcat62_n00110 fcatZZs16_n00111).get k = (FCat.node fcat62_n00110 fcat62_n00111).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq_3132_5 (k / 2) (by omega) (by omega)

theorem eq_3132_3 : ∀ k, k < 512 → k ≠ 391 → fcatZZs16_n001.get k = fcat62_n001.get k := by
  intro k hk hne
  show (FCat.node fcat62_n0010 fcatZZs16_n0011).get k = (FCat.node fcat62_n0010 fcat62_n0011).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq_3132_4 (k / 2) (by omega) (by omega)

theorem eq_3132_2 : ∀ k, k < 1024 → k ≠ 783 → fcatZZs16_n00.get k = fcat62_n00.get k := by
  intro k hk hne
  show (FCat.node fcat62_n000 fcatZZs16_n001).get k = (FCat.node fcat62_n000 fcat62_n001).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq_3132_3 (k / 2) (by omega) (by omega)

theorem eq_3132_1 : ∀ k, k < 2048 → k ≠ 1566 → fcatZZs16_n0.get k = fcat62_n0.get k := by
  intro k hk hne
  show (FCat.node fcatZZs16_n00 fcat62_n01).get k = (FCat.node fcat62_n00 fcat62_n01).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq_3132_2 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq0 : ∀ k, k < 4096 → k ≠ 3131 → k ≠ 3132 → fcatZZs16.get k = fcat62.get k := by
  intro k hk h1 h2
  show (FCat.node fcatZZs16_n0 fcatZZs16_n1).get k = (FCat.node fcat62_n0 fcat62_n1).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq_3132_1 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]
    exact eq_3131_1 (k / 2) (by omega) (by omega)

theorem get_eq (r : ℕ) (hr : r < 3131) : fcatZZs16.get r = fcat62.get r := eq0 r (by omega) (by omega) (by omega)

theorem zlist : (fcatZZs16.get 3131).1 = OmissionZRow.zIndices := by decide +kernel
theorem zdem : fcatZZs16.dem 3131 = 16 := by decide +kernel
theorem zslist : (fcatZZs16.get 3132).1 = OmissionZStarRow.zsIndices := by decide +kernel
theorem zsdem : fcatZZs16.dem 3132 = 16 := by decide +kernel

theorem zsupp : fsupp fcatZZs16 252 3131 = OmissionZRow.Z := by
  ext i
  rw [OmissionZRow.Z_eq]
  simp only [fsupp, Finset.mem_filter, Finset.mem_univ, true_and, zlist]

theorem zssupp : fsupp fcatZZs16 252 3132 = OmissionZStarRow.Zs := by
  ext i
  rw [OmissionZStarRow.Zs_eq]
  simp only [fsupp, Finset.mem_filter, Finset.mem_univ, true_and, zslist]

/-- Every row of `fcatZZs16` holds for a 0/1 vector that satisfies the 2,685 base rows and both Z-rows at 16. -/
theorem fcatZZs16_rows (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i)
    (hz : 16 ≤ ∑ i ∈ OmissionZRow.Z, holes i) (hzs : 16 ≤ ∑ i ∈ OmissionZStarRow.Zs, holes i) :
    ∀ r : Fin 3133, fcatZZs16.dem r.val ≤ ∑ i ∈ fsupp fcatZZs16 252 r.val, holes i := by
  intro ⟨r, hr⟩
  by_cases h : r < 3131
  · have h62 := CompactChecker.Bridge311Bal.fcat62_rows holes hbool hrows ⟨r, h⟩
    have hd : fcatZZs16.dem r = fcat62.dem r := by unfold FCat.dem; rw [get_eq r h]
    have hs : fsupp fcatZZs16 252 r = fsupp fcat62 252 r := by unfold fsupp; rw [get_eq r h]
    show fcatZZs16.dem r ≤ ∑ i ∈ fsupp fcatZZs16 252 r, holes i
    rw [hd, hs]
    exact h62
  · by_cases h' : r = 3131
    · subst h'
      show fcatZZs16.dem 3131 ≤ ∑ i ∈ fsupp fcatZZs16 252 3131, holes i
      rw [zsupp, zdem]
      exact hz
    · have e : r = 3132 := by omega
      subst e
      show fcatZZs16.dem 3132 ≤ ∑ i ∈ fsupp fcatZZs16 252 3132, holes i
      rw [zssupp, zsdem]
      exact hzs

/-- The bridge: the zero-side root exclusion of the compact export over `fcatZZs16` (state 0 occupied) gives
`OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 budget`. -/
theorem zzsn16_of_root {budget : ℕ}
    (h : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZZs16 3133 252 budget (pmask (zerosF 252) [(0, 2)]) holes) :
    OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 budget := by
  rintro ⟨holes, h0, _, hb, hr, _, hz, hzs, hc⟩
  refine h ⟨holes, hb, fcatZZs16_rows holes hb hr hz hzs, hc, fun i hi => ?_, fun i hi => ?_⟩
  · rcases mem_mset_zero_occupied 1 i hi with ⟨_, h12⟩ | h10
    · exact absurd h12 (by decide)
    · exact absurd h10 (by decide)
  · rcases mem_mset_zero_occupied 2 i hi with ⟨hi0, _⟩ | h20
    · have : i = 0 := Fin.ext hi0
      subst this
      exact h0
    · exact absurd h20 (by decide)

#print axioms get_eq
#print axioms zsupp
#print axioms zssupp
#print axioms fcatZZs16_rows
#print axioms zzsn16_of_root

end CompactChecker.BridgeZZs16
