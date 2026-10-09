import ErdosSzekeres.OmissionCertificates

/-!
# Rounded arithmetic cover cuts

These lemmas justify additional cardinality inequalities from previously proved
omission rows. They do not add geometric hypotheses or trust a numerical solver.
The supplied nonnegative integer weights and the strict margin are checked by
ordinary Lean arithmetic.
-/

namespace ErdosSzekeres.OmissionCertificates

open scoped BigOperators

/-- A weighted collection of omission rows bounds the number of holes in any
chosen subset. Columns outside the subset are paid for using the Boolean upper
bound; columns inside it receive the stated capacity. -/
theorem weighted_subset_capacity_bound {ι ρ : Type*} [Fintype ι] [Fintype ρ]
    [DecidableEq ι] (support : ρ → Finset ι) (demand weight : ρ → ℕ)
    (holes : ι → ℕ) (s : Finset ι) (capacity : ℕ)
    (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r, demand r ≤ ∑ i ∈ support r, holes i) :
    ∑ r, weight r * demand r ≤
      capacity * (∑ i ∈ s, holes i) +
        ∑ i, (load support weight i - if i ∈ s then capacity else 0) := by
  classical
  have transpose : (∑ r, weight r * ∑ i ∈ support r, holes i) =
      ∑ i, load support weight i * holes i := by
    simp only [load, Finset.sum_mul, Finset.mul_sum, ite_mul, zero_mul]
    rw [Finset.sum_comm]
    congr 1
    funext r
    simp
  calc
    ∑ r, weight r * demand r ≤ ∑ r, weight r * ∑ i ∈ support r, holes i :=
      Finset.sum_le_sum fun r _ => Nat.mul_le_mul_left _ (hrows r)
    _ = ∑ i, load support weight i * holes i := transpose
    _ ≤ ∑ i, ((if i ∈ s then capacity * holes i else 0) +
        (load support weight i - if i ∈ s then capacity else 0)) := by
      apply Finset.sum_le_sum
      intro i _
      have hi := hbool i
      have hz : holes i = 0 ∨ holes i = 1 := by omega
      rcases hz with hz | hz <;> by_cases hs : i ∈ s <;> simp [hz, hs]
      omega
    _ = capacity * (∑ i ∈ s, holes i) +
        ∑ i, (load support weight i - if i ∈ s then capacity else 0) := by
      rw [Finset.sum_add_distrib]
      congr 1
      simp [Finset.mul_sum]

/-- A strict integer weighted margin proves a rounded cover inequality. This
is a certificate for a new row, not merely a floating-point lower bound. -/
theorem rounded_cover_cut {ι ρ : Type*} [Fintype ι] [Fintype ρ]
    [DecidableEq ι] (support : ρ → Finset ι) (demand weight : ρ → ℕ)
    (s : Finset ι) (capacity target : ℕ)
    (hmargin : capacity * (target - 1) +
        ∑ i, (load support weight i - if i ∈ s then capacity else 0) <
      ∑ r, weight r * demand r)
    (holes : ι → ℕ) (hbool : ∀ i, holes i ≤ 1)
    (hrows : ∀ r, demand r ≤ ∑ i ∈ support r, holes i) :
    target ≤ ∑ i ∈ s, holes i := by
  by_contra hn
  have hs : (∑ i ∈ s, holes i) ≤ target - 1 := by omega
  have hb := Nat.mul_le_mul_left capacity hs
  have hw := weighted_subset_capacity_bound support demand weight holes s capacity hbool hrows
  omega

#print axioms weighted_subset_capacity_bound
#print axioms rounded_cover_cut

end ErdosSzekeres.OmissionCertificates
