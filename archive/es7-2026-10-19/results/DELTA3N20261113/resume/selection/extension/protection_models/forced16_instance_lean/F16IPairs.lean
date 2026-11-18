import F16IAggregate

namespace Delta3.Forced16Instance

open Delta3.Forced16Algebra Lean.Grind Std

variable {K : Type u} [CommRing K]

theorem monomial_indicator (vs : List Nat) (x : Nat → K) (j : Nat)
    (hn : vs.Nodup) (hj : j ∈ vs) :
    monomial vs x (fun k => if k = j then 1 else 0) = x j := by
  induction vs with
  | nil => simp at hj
  | cons a vs ih =>
    have hnd := List.nodup_cons.mp hn
    by_cases h : a = j
    · subst a
      have hz : monomial vs x (fun k => if k = j then 1 else 0) = 1 := by
        apply (monomial_congr vs x _ (fun _ => 0) ?_).trans (monomial_zero vs x)
        intro k hk
        have hkj : k ≠ j := by
          intro he
          subst k
          exact hnd.1 hk
        simp only [if_neg hkj]
      change x j ^ (if j = j then 1 else 0) *
        monomial vs x (fun k => if k = j then 1 else 0) = x j
      rw [if_pos rfl, Semiring.pow_one, hz, Semiring.mul_one]
    · have hj' : j ∈ vs := by
        rcases List.mem_cons.mp hj with he | he
        · exact False.elim (h he.symm)
        · exact he
      change x a ^ (if a = j then 1 else 0) *
        monomial vs x (fun k => if k = j then 1 else 0) = x j
      rw [if_neg h, Semiring.pow_zero, Semiring.one_mul]
      exact ih hnd.2 hj'

theorem monomial_pair (vs : List Nat) (x : Nat → K) (i j : Nat)
    (hn : vs.Nodup) (hi : i ∈ vs) (hj : j ∈ vs) :
    monomial vs x (fun k => (if k = i then 1 else 0) + (if k = j then 1 else 0)) =
      x i * x j := by
  rw [monomial_add, monomial_indicator vs x i hn hi, monomial_indicator vs x j hn hj]

set_option maxRecDepth 10000
set_option maxHeartbeats 10000000

theorem factors_bounded : rows.all (fun r => decide
    (r.small1 < 560 ∧ r.small2 < 560 ∧ r.large1 < 560 ∧ r.large2 < 560)) = true := by
  decide +kernel

theorem small_monomial (r : Row) (hr : r ∈ rows) (x : Nat → K) :
    monomial vars x (smallExp r) = x r.small1 * x r.small2 := by
  have hb := _root_.of_decide_eq_true (List.all_eq_true.mp factors_bounded r hr)
  exact monomial_pair vars x r.small1 r.small2 (List.nodup_range (n := 560))
    (List.mem_range.mpr hb.1) (List.mem_range.mpr hb.2.1)

theorem large_monomial (r : Row) (hr : r ∈ rows) (x : Nat → K) :
    monomial vars x (largeExp r) = x r.large1 * x r.large2 := by
  have hb := _root_.of_decide_eq_true (List.all_eq_true.mp factors_bounded r hr)
  exact monomial_pair vars x r.large1 r.large2 (List.nodup_range (n := 560))
    (List.mem_range.mpr hb.2.2.1) (List.mem_range.mpr hb.2.2.2)

/-- The exact fixed product-inequality system is infeasible over any ordered ring of this type.
No premise asserts that the variables are determinants or that coordinate signs imply the rows. -/
theorem no_positive_product_assignment [LE K] [LT K] [LawfulOrderLT K]
    [IsLinearOrder K] [OrderedRing K] (x : Nat → K)
    (hx : ∀ j ∈ vars, 0 < x j)
    (hlt : ∀ r ∈ rows, x r.small1 * x r.small2 < x r.large1 * x r.large2) : False := by
  apply no_positive_monomial_assignment x hx
  intro r hr
  rw [small_monomial r hr x, large_monomial r hr x]
  exact hlt r hr

#print axioms monomial_indicator
#print axioms monomial_pair
#print axioms factors_bounded
#print axioms small_monomial
#print axioms large_monomial
#print axioms no_positive_product_assignment

end Delta3.Forced16Instance
