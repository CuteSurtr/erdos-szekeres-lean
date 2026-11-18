import Mathlib.Algebra.Order.Field.Defs
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Finset.Lattice.Fold

/-!
# Finite affine envelopes on the nonnegative ray

DRAFT STATEMENTS ONLY: intentionally unfinished `by done` proofs.
Import verification exceeded the authorized resident-memory guard; no theorem here is a
finished Lean result. This generic ordered-field formulation specializes mathematically to
real affine lines but does not itself import or verify the real-number specialization.
Pure affine algebra; no assertion about point configurations or Delta selection.
-/

namespace Delta3.Envelope

open scoped BigOperators

/-- An affine line, with height measured at parameter zero. -/
structure Line (K : Type*) where
  slope : K
  height : K

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

/-- Evaluation at the ordered-field parameter `t`. -/
def Line.eval (L : Line K) (t : K) : K := L.slope * t + L.height

/-- The maximum of a finite nonempty family of line values. -/
def envelope {ι : Type*} (s : Finset ι) (hs : s.Nonempty) (L : ι → Line K) (t : K) : K :=
  s.sup' hs (fun i ↦ (L i).eval t)

/-- Evaluation commutes with a finite weighted sum of coefficient pairs. -/
theorem sum_weighted_eval {ι : Type*} (s : Finset ι) (L : ι → Line K) (w : ι → K) (t : K) :
    (∑ i ∈ s, w i * (L i).eval t) =
      (∑ i ∈ s, w i * (L i).slope) * t + ∑ i ∈ s, w i * (L i).height := by
  done

/-- The coefficient certificate bounds the target by any common upper bound of its supports. -/
theorem le_upper_of_weighted_certificate {ι : Type*} (s : Finset ι) (L : ι → Line K)
    (q : Line K) (w : ι → K) (hw : ∀ i ∈ s, 0 ≤ w i) (hunit : ∑ i ∈ s, w i = 1)
    (hslope : q.slope ≤ ∑ i ∈ s, w i * (L i).slope)
    (hheight : q.height ≤ ∑ i ∈ s, w i * (L i).height)
    {t M : K} (ht : 0 ≤ t) (hM : ∀ i ∈ s, (L i).eval t ≤ M) : q.eval t ≤ M := by
  done

/-- Nonnegative weights with unit sum and dominating coefficients certify the entire ray. -/
theorem le_envelope_of_weighted_certificate {ι : Type*} (s : Finset ι) (hs : s.Nonempty)
    (L : ι → Line K) (q : Line K) (w : ι → K) (hw : ∀ i ∈ s, 0 ≤ w i)
    (hunit : ∑ i ∈ s, w i = 1)
    (hslope : q.slope ≤ ∑ i ∈ s, w i * (L i).slope)
    (hheight : q.height ≤ ∑ i ∈ s, w i * (L i).height)
    {t : K} (ht : 0 ≤ t) : q.eval t ≤ envelope s hs L t := by
  done

/-- A two-line convex coefficient certificate suffices. -/
theorem le_max_of_two_supports (q A B : Line K) {w : K} (hw : 0 ≤ w) (hw1 : w ≤ 1)
    (hslope : q.slope ≤ w * A.slope + (1 - w) * B.slope)
    (hheight : q.height ≤ w * A.height + (1 - w) * B.height)
    {t : K} (ht : 0 ≤ t) : q.eval t ≤ max (A.eval t) (B.eval t) := by
  done

/-- Finite universal domination admits a coefficient certificate using at most two supports.
Repeated indices and endpoint weights include the single-support case. -/
theorem exists_two_supports_of_le_envelope {ι : Type*} (s : Finset ι) (hs : s.Nonempty)
    (L : ι → Line K) (q : Line K)
    (h : ∀ t : K, 0 ≤ t → q.eval t ≤ envelope s hs L t) :
    ∃ i ∈ s, ∃ j ∈ s, ∃ w : K, 0 ≤ w ∧ w ≤ 1 ∧
      q.slope ≤ w * (L i).slope + (1 - w) * (L j).slope ∧
      q.height ≤ w * (L i).height + (1 - w) * (L j).height := by
  done

namespace Example

def q : Line K := ⟨-2, -4⟩
def L24 : Line K := ⟨-3 / 2, -15 / 2⟩
def L56 : Line K := ⟨-12, -14⟩
def L57 (h : K) : Line K := ⟨(h - 10) / 2, h⟩

def F (h t : K) : K := max (L24.eval t) (max (L56.eval t) ((L57 h).eval t))

theorem half_sum (t : K) : (L24.eval t + (L57 5).eval t) / 2 = q.eval t + 11 / 4 := by
  done

theorem safe_at_five (t : K) (ht : 0 ≤ t) : q.eval t + 11 / 4 ≤ F 5 t := by
  done

theorem no_single_support_at_five :
    (∃ t : K, 0 < t ∧ L24.eval t < q.eval t) ∧
    (∃ t : K, 0 < t ∧ L56.eval t < q.eval t) ∧
    (∃ t : K, 0 < t ∧ (L57 5).eval t < q.eval t) := by
  done

theorem exposure_at_three_iff (t : K) : F 3 t < q.eval t ↔ 14 / 3 < t ∧ t < 7 := by
  done

theorem exposure_at_six :
    F (K := K) 3 6 = -33 / 2 ∧ (q (K := K)).eval 6 = -16 ∧
      F (K := K) 3 6 < q.eval 6 := by
  done

end Example
end Delta3.Envelope
