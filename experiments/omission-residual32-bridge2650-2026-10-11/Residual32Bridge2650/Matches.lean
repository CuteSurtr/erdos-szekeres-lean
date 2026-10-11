import Residual32Bridge2650.Catalog
import Residual32ContextsProof.Catalog
import AddedRows
import SixthRelaxedProof.Data
import RankCoreOne
import RankCoreTwo
import RankCoreThree
import RankCoreFour

/-!
Literal binding of the 2,650 catalog rows to the existing row families.

Every equality below is decided by the kernel on the literal data; no row order
or metadata from the search is trusted. Zero-based blocks of `source-2650.json.gz`:

* rows 0–2468: the frozen 2,469-row catalog `OmissionResidual32Contexts`;
* rows 2469–2597: `Residual32AddedRows.support` (Sixth core, then Fourth family);
* rows 2598–2645: `CoupledSixthRelaxedVariants.support`;
* rows 2646–2649: the supports of `CoupledCoreRankSearch{One,Two,Three,Four}`.

Every row from 2469 on has demand one.
-/

open ErdosSzekeres ErdosSzekeres.Omission ErdosSzekeres.OmissionCertificates

namespace OmissionResidual32Bridge2650

set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

def prefixIndex (r : Fin 2469) : Fin 2650 := ⟨r.val, by omega⟩
def addedIndex (r : Fin 129) : Fin 2650 := ⟨2469 + r.val, by omega⟩
def relaxedIndex (r : Fin 48) : Fin 2650 := ⟨2598 + r.val, by omega⟩
def suffixIndex (r : Fin 181) : Fin 2650 := ⟨2469 + r.val, by omega⟩

/-- Row `r` of the new catalog equals row `r` of the frozen 2,469-row catalog. -/
abbrev PrefixRow (r : ℕ) (h : r < 2469) : Prop :=
  support2650 ⟨r, by omega⟩ = OmissionResidual32Contexts.support ⟨r, h⟩ ∧
  demand2650 ⟨r, by omega⟩ = OmissionResidual32Contexts.demand ⟨r, h⟩

theorem PrefixRow.congr {a b : ℕ} (e : a = b) {ha : a < 2469} {hb : b < 2469}
    (h : PrefixRow a ha) : PrefixRow b hb := by
  subst e
  exact h

/-! The prefix is decided in 128-row chunks, one kernel declaration each, which
keeps the kernel's working memory per declaration small. -/

theorem prefix_chunk0 : ∀ j (hj : j < 128), PrefixRow (0 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk1 : ∀ j (hj : j < 128), PrefixRow (128 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk2 : ∀ j (hj : j < 128), PrefixRow (256 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk3 : ∀ j (hj : j < 128), PrefixRow (384 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk4 : ∀ j (hj : j < 128), PrefixRow (512 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk5 : ∀ j (hj : j < 128), PrefixRow (640 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk6 : ∀ j (hj : j < 128), PrefixRow (768 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk7 : ∀ j (hj : j < 128), PrefixRow (896 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk8 : ∀ j (hj : j < 128), PrefixRow (1024 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk9 : ∀ j (hj : j < 128), PrefixRow (1152 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk10 : ∀ j (hj : j < 128), PrefixRow (1280 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk11 : ∀ j (hj : j < 128), PrefixRow (1408 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk12 : ∀ j (hj : j < 128), PrefixRow (1536 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk13 : ∀ j (hj : j < 128), PrefixRow (1664 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk14 : ∀ j (hj : j < 128), PrefixRow (1792 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk15 : ∀ j (hj : j < 128), PrefixRow (1920 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk16 : ∀ j (hj : j < 128), PrefixRow (2048 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk17 : ∀ j (hj : j < 128), PrefixRow (2176 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk18 : ∀ j (hj : j < 128), PrefixRow (2304 + j) (by omega) := by
  decide +kernel

theorem prefix_chunk19 : ∀ j (hj : j < 37), PrefixRow (2432 + j) (by omega) := by
  decide +kernel

/-- Rows 0–2468 are exactly the frozen 2,469-row catalog. -/
theorem prefix_matches : ∀ r : Fin 2469,
    support2650 (prefixIndex r) = OmissionResidual32Contexts.support r ∧
    demand2650 (prefixIndex r) = OmissionResidual32Contexts.demand r := by
  intro ⟨r, hr⟩
  show PrefixRow r hr
  obtain ⟨k, hk, j, hj, rfl⟩ : ∃ k < 20, ∃ j < 128, r = 128 * k + j :=
    ⟨r / 128, by omega, r % 128, Nat.mod_lt _ (by omega), by omega⟩
  interval_cases k
  · exact PrefixRow.congr (by omega) (prefix_chunk0 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk1 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk2 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk3 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk4 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk5 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk6 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk7 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk8 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk9 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk10 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk11 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk12 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk13 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk14 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk15 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk16 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk17 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk18 j (by omega))
  · exact PrefixRow.congr (by omega) (prefix_chunk19 j (by omega))

/-- Rows 2469–2597 are the 129 literal supports of `Residual32AddedRows`. -/
theorem added_matches : ∀ r : Fin 129,
    support2650 (addedIndex r) = Residual32AddedRows.support r ∧
    demand2650 (addedIndex r) = 1 := by
  decide +kernel

/-- Rows 2598–2645 are the 48 relaxed Sixth-template supports. -/
theorem relaxed_matches : ∀ r : Fin 48,
    support2650 (relaxedIndex r) = CoupledSixthRelaxedVariants.support r ∧
    demand2650 (relaxedIndex r) = 1 := by
  decide +kernel

/-- Row 2646 is the first attained-rank coupled core. -/
theorem rank_one_matches :
    support2650 ⟨2646, by decide⟩ = CoupledCoreRankSearchOne.support.toFinset ∧
    demand2650 ⟨2646, by decide⟩ = 1 := by
  decide +kernel

/-- Row 2647 is the second attained-rank coupled core. -/
theorem rank_two_matches :
    support2650 ⟨2647, by decide⟩ = CoupledCoreRankSearchTwo.support.toFinset ∧
    demand2650 ⟨2647, by decide⟩ = 1 := by
  decide +kernel

/-- Row 2648 is the third attained-rank coupled core. -/
theorem rank_three_matches :
    support2650 ⟨2648, by decide⟩ = CoupledCoreRankSearchThree.support.toFinset ∧
    demand2650 ⟨2648, by decide⟩ = 1 := by
  decide +kernel

/-- Row 2649 is the fourth attained-rank coupled core. -/
theorem rank_four_matches :
    support2650 ⟨2649, by decide⟩ = CoupledCoreRankSearchFour.support.toFinset ∧
    demand2650 ⟨2649, by decide⟩ = 1 := by
  decide +kernel

/-- Every row from 2469 on has demand one. -/
theorem suffix_demand : ∀ r : Fin 181, demand2650 (suffixIndex r) = 1 := by
  decide +kernel

/-- The sparse row code `rowCode b s = ∑ i ∈ s, b ^ i` as a packed indicator. -/
theorem rowCode_eq_pack {n : ℕ} (b : ℕ) (s : Finset (Fin n)) :
    rowCode b s = pack b (fun i => if i ∈ s then 1 else 0) := by
  simp only [rowCode, pack, ite_mul, one_mul, zero_mul]
  rw [Finset.sum_ite_mem, Finset.univ_inter]

/-- Row codes determine supports for every base above one. -/
theorem rowCode_injective {n b : ℕ} (hb : 1 < b) {s t : Finset (Fin n)}
    (h : rowCode b s = rowCode b t) : s = t := by
  rw [rowCode_eq_pack, rowCode_eq_pack] at h
  have hf := pack_injective_of_lt hb
    (fun i => by by_cases hi : i ∈ s <;> simp [hi] <;> omega)
    (fun i => by by_cases hi : i ∈ t <;> simp [hi] <;> omega) h
  ext i
  have hi := congrFun hf i
  by_cases hs : i ∈ s <;> by_cases ht : i ∈ t <;> simp_all

/-- Support equality for another literal catalog `support'` with checked codes
`code'` in any base `b > 1`: it suffices that `code' r = rowCode b (support2650 r)`. -/
theorem support2650_eq_of_rowCode {b : ℕ} (hb : 1 < b)
    {support' : Fin 2650 → Finset (Fin 154)} {code' : Fin 2650 → ℕ}
    (hcode' : ∀ r, code' r = rowCode b (support' r))
    (hcode : ∀ r, code' r = rowCode b (support2650 r)) :
    ∀ r, support' r = support2650 r := fun r =>
  rowCode_injective hb ((hcode' r).symm.trans (hcode r))

/-- The same for a catalog exported with this catalog's base `2 ^ 17`: equal packed
codes (a cheap `decide +kernel` over big integers) give equal supports. -/
theorem support2650_eq_of_codes {support' : Fin 2650 → Finset (Fin 154)}
    {code' : Fin 2650 → ℕ} (hcode' : ∀ r, code' r = rowCode base (support' r))
    (hcodes : ∀ r, code' r = code r) : ∀ r, support' r = support2650 r :=
  support2650_eq_of_rowCode (by decide) hcode' fun r => (hcodes r).trans (code_correct r)

#print axioms rowCode_injective
#print axioms support2650_eq_of_rowCode
#print axioms support2650_eq_of_codes
#print axioms prefix_matches
#print axioms added_matches
#print axioms relaxed_matches
#print axioms rank_one_matches
#print axioms rank_two_matches
#print axioms rank_three_matches
#print axioms rank_four_matches
#print axioms suffix_demand

end OmissionResidual32Bridge2650
