-- FV304 (20 November 2026): the bridge from the compact check over fcatZ to ExcludesHoleBudgetZ.
import CompactChecker.Path
import CompactChecker.FcatZ
import CompactChecker.Bridge311Bal
import LemmaZ

/-!
# Fcat bridge for the Lean check of the ES(8) ≤ 304 tree (FV304, 20 November 2026)

`fcatZ` (CompactChecker/FcatZ.lean) is `fcat62` with the Z-row added as row 3131; every subtree off the path to
row 3131 is `fcat62`'s own constant. So `fcatZ.get r = fcat62.get r` for r < 3131 (`get_eq`, by the 12 path
levels), the 3,131 shared rows hold by `Bridge311Bal.fcat62_rows` (the ES(8) ≤ 311/310 bridge), and row 3131 is
the Z-row: support `OmissionZRow.Z` (`zsupp`, from `OmissionZRow.Z_eq` and the literal `zIndices`), demand 15.
`balanced_z_of_root` turns the root exclusion of the compact export over `fcatZ` into the body of
`OmissionBalancedZ.ExcludesHoleBudgetZ budget` (ES305N20261119/BalancedBudgetsZ.lean).
-/

open ErdosSzekeres.OmissionCertificates
open scoped BigOperators

namespace CompactChecker.BridgeZ

theorem node_get_even {l r : FCat} {k : ℕ} (h : k % 2 = 0) : (FCat.node l r).get k = l.get (k / 2) := by
  show (bif Nat.beq (k % 2) 0 then l.get (k / 2) else r.get (k / 2)) = l.get (k / 2)
  rw [h]; rfl

theorem node_get_odd {l r : FCat} {k : ℕ} (h : k % 2 = 1) : (FCat.node l r).get k = r.get (k / 2) := by
  show (bif Nat.beq (k % 2) 0 then l.get (k / 2) else r.get (k / 2)) = r.get (k / 2)
  rw [h]; rfl

/-- Level 11 (the new node): index 0 is row 1083 in both catalogs. -/
theorem eq11 : ∀ k, k < 2 → k ≠ 1 → fcatZ_n11011100001.get k = fcat62_r1083.get k := by
  intro k hk hne
  obtain rfl : k = 0 := by omega
  rfl

theorem eq10 : ∀ k, k < 4 → k ≠ 3 → fcatZ_n1101110000.get k = fcat62_n1101110000.get k := by
  intro k hk hne
  show (FCat.node fcat62_n11011100000 fcatZ_n11011100001).get k = (FCat.node fcat62_n11011100000 fcat62_r1083).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq11 (k / 2) (by omega) (by omega)

theorem eq9 : ∀ k, k < 8 → k ≠ 6 → fcatZ_n110111000.get k = fcat62_n110111000.get k := by
  intro k hk hne
  show (FCat.node fcatZ_n1101110000 fcat62_n1101110001).get k = (FCat.node fcat62_n1101110000 fcat62_n1101110001).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq10 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq8 : ∀ k, k < 16 → k ≠ 12 → fcatZ_n11011100.get k = fcat62_n11011100.get k := by
  intro k hk hne
  show (FCat.node fcatZ_n110111000 fcat62_n110111001).get k = (FCat.node fcat62_n110111000 fcat62_n110111001).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq9 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq7 : ∀ k, k < 32 → k ≠ 24 → fcatZ_n1101110.get k = fcat62_n1101110.get k := by
  intro k hk hne
  show (FCat.node fcatZ_n11011100 fcat62_n11011101).get k = (FCat.node fcat62_n11011100 fcat62_n11011101).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq8 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq6 : ∀ k, k < 64 → k ≠ 48 → fcatZ_n110111.get k = fcat62_n110111.get k := by
  intro k hk hne
  show (FCat.node fcatZ_n1101110 fcat62_n1101111).get k = (FCat.node fcat62_n1101110 fcat62_n1101111).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq7 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq5 : ∀ k, k < 128 → k ≠ 97 → fcatZ_n11011.get k = fcat62_n11011.get k := by
  intro k hk hne
  show (FCat.node fcat62_n110110 fcatZ_n110111).get k = (FCat.node fcat62_n110110 fcat62_n110111).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq6 (k / 2) (by omega) (by omega)

theorem eq4 : ∀ k, k < 256 → k ≠ 195 → fcatZ_n1101.get k = fcat62_n1101.get k := by
  intro k hk hne
  show (FCat.node fcat62_n11010 fcatZ_n11011).get k = (FCat.node fcat62_n11010 fcat62_n11011).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq5 (k / 2) (by omega) (by omega)

theorem eq3 : ∀ k, k < 512 → k ≠ 391 → fcatZ_n110.get k = fcat62_n110.get k := by
  intro k hk hne
  show (FCat.node fcat62_n1100 fcatZ_n1101).get k = (FCat.node fcat62_n1100 fcat62_n1101).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq4 (k / 2) (by omega) (by omega)

theorem eq2 : ∀ k, k < 1024 → k ≠ 782 → fcatZ_n11.get k = fcat62_n11.get k := by
  intro k hk hne
  show (FCat.node fcatZ_n110 fcat62_n111).get k = (FCat.node fcat62_n110 fcat62_n111).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
    exact eq3 (k / 2) (by omega) (by omega)
  · rw [node_get_odd h, node_get_odd h]

theorem eq1 : ∀ k, k < 2048 → k ≠ 1565 → fcatZ_n1.get k = fcat62_n1.get k := by
  intro k hk hne
  show (FCat.node fcat62_n10 fcatZ_n11).get k = (FCat.node fcat62_n10 fcat62_n11).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq2 (k / 2) (by omega) (by omega)

theorem eq0 : ∀ k, k < 4096 → k ≠ 3131 → fcatZ.get k = fcat62.get k := by
  intro k hk hne
  show (FCat.node fcat62_n0 fcatZ_n1).get k = (FCat.node fcat62_n0 fcat62_n1).get k
  rcases Nat.mod_two_eq_zero_or_one k with h | h
  · rw [node_get_even h, node_get_even h]
  · rw [node_get_odd h, node_get_odd h]
    exact eq1 (k / 2) (by omega) (by omega)

theorem get_eq (r : ℕ) (hr : r < 3131) : fcatZ.get r = fcat62.get r := eq0 r (by omega) (by omega)

/-- Row 3131 of `fcatZ` is the Z-row: support `OmissionZRow.Z`, demand 15. -/
theorem zlist : (fcatZ.get 3131).1 = OmissionZRow.zIndices := by decide +kernel

theorem zdem : fcatZ.dem 3131 = 15 := by decide +kernel

theorem zsupp : fsupp fcatZ 252 3131 = OmissionZRow.Z := by
  ext i
  rw [OmissionZRow.Z_eq]
  simp only [fsupp, Finset.mem_filter, Finset.mem_univ, true_and, zlist]

/-- Every row of `fcatZ` holds for a 0/1 vector that satisfies the 2,685 rows of `BalancedProof.Catalog`
and the Z-row. -/
theorem fcatZ_rows (holes : Fin 252 → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r : Fin 2685, OmissionBalanced.demand r ≤
      ∑ i ∈ OmissionBalanced.support r, holes i)
    (hz : 15 ≤ ∑ i ∈ OmissionZRow.Z, holes i) :
    ∀ r : Fin 3132, fcatZ.dem r.val ≤ ∑ i ∈ fsupp fcatZ 252 r.val, holes i := by
  intro ⟨r, hr⟩
  by_cases h : r < 3131
  · have h62 := CompactChecker.Bridge311Bal.fcat62_rows holes hbool hrows ⟨r, h⟩
    have hd : fcatZ.dem r = fcat62.dem r := by unfold FCat.dem; rw [get_eq r h]
    have hs : fsupp fcatZ 252 r = fsupp fcat62 252 r := by unfold fsupp; rw [get_eq r h]
    show fcatZ.dem r ≤ ∑ i ∈ fsupp fcatZ 252 r, holes i
    rw [hd, hs]
    exact h62
  · have e : r = 3131 := by omega
    subst e
    show fcatZ.dem 3131 ≤ ∑ i ∈ fsupp fcatZ 252 3131, holes i
    rw [zsupp, zdem]
    exact hz

/-- The Fcat bridge: the root exclusion of the compact export over `fcatZ` gives the body of
`OmissionBalancedZ.ExcludesHoleBudgetZ budget`. -/
theorem balanced_z_of_root {budget : ℕ}
    (h : ¬ ∃ holes : Fin 252 → ℕ, FFeas fcatZ 3132 252 budget (pmask (zerosF 252) []) holes) :
    ¬ ∃ holes : Fin 252 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, OmissionBalanced.demand r ≤ ∑ i ∈ OmissionBalanced.support r, holes i) ∧
      (∀ r, BalancedCoverCutsV2.demand r ≤ ∑ i ∈ BalancedCoverCutsV2.support r, holes i) ∧
      15 ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ (∑ i, holes i) ≤ budget := by
  rintro ⟨holes, hb, hr, _, hz, hc⟩
  refine h ⟨holes, hb, fcatZ_rows holes hb hr hz, hc, fun i hi => ?_, fun i hi => ?_⟩
  · rw [mset_zeros 252 1 (by decide)] at hi
    exact absurd hi (Finset.notMem_empty i)
  · rw [mset_zeros 252 2 (by decide)] at hi
    exact absurd hi (Finset.notMem_empty i)

#print axioms get_eq
#print axioms zsupp
#print axioms fcatZ_rows
#print axioms balanced_z_of_root

end CompactChecker.BridgeZ
