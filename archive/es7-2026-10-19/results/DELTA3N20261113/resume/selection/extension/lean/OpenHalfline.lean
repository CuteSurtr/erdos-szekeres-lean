import WeightedEnvelope

/-! Open-ray domination for a finite affine envelope extends to parameter zero. -/

namespace Delta3.WeightedEnvelope

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

omit [Field K] [IsStrictOrderedRing K] in
theorem maxFrom_le {ι : Type*} (base M : K) (s : List ι) (f : ι → K)
    (hb : base ≤ M) (hs : ∀ i ∈ s, f i ≤ M) : maxFrom base s f ≤ M :=
  List.recOn (motive := fun s ↦ (∀ i ∈ s, f i ≤ M) → maxFrom base s f ≤ M) s
    (fun _ ↦ hb)
    (fun i rest ih h ↦ max_le (h i (.head rest)) (ih fun j hj ↦ h j (.tail i hj))) hs

/-- A finite affine envelope dominating at every positive parameter also dominates at zero. -/
theorem le_envelope_zero_of_pos {ι : Type*} (first : ι) (rest : List ι)
    (L : ι → Line K) (q : Line K)
    (h : ∀ t : K, 0 < t → q.eval t ≤ envelope first rest L t) :
    q.eval 0 ≤ envelope first rest L 0 := by
  by_contra hn
  let H := envelope first rest L 0
  let S := maxFrom 0 (first :: rest) (fun i ↦ (L i).slope - q.slope)
  let D := q.eval 0 - H
  have hD : 0 < D := sub_pos.mpr (lt_of_not_ge hn)
  have hS : 0 ≤ S := le_maxFrom_base 0 (first :: rest) _
  have hden : 0 < S + 1 := add_pos_of_nonneg_of_pos hS zero_lt_one
  let t := D / (S + 1)
  have ht : 0 < t := div_pos hD hden
  have hid : (S + 1) * t = D := mul_div_cancel₀ D hden.ne'
  have hst : S * t < D := by
    rw [add_mul, one_mul] at hid
    exact (lt_add_of_pos_right (S * t) ht).trans_eq hid
  have hslope : ∀ i ∈ first :: rest, (L i).slope ≤ q.slope + S := fun i hi ↦
    ((sub_le_iff_le_add).mp
      (le_maxFrom_of_mem 0 (first :: rest) (fun j ↦ (L j).slope - q.slope) i hi)).trans_eq
      (add_comm S q.slope)
  have hheight : ∀ i ∈ first :: rest, (L i).height ≤ H := fun i hi ↦ by
    simpa only [Line.eval, mul_zero, zero_add] using eval_le_envelope first rest L 0 i hi
  have hu : ∀ i ∈ first :: rest, (L i).eval t ≤ (q.slope + S) * t + H :=
    fun i hi ↦ add_le_add (mul_le_mul_of_nonneg_right (hslope i hi) ht.le) (hheight i hi)
  have henv : envelope first rest L t ≤ (q.slope + S) * t + H :=
    maxFrom_le _ _ rest _ (hu first (.head rest)) (fun i hi ↦ hu i (.tail first hi))
  have htarget := (h t ht).trans henv
  have hheight' : q.height ≤ S * t + H :=
    (add_le_add_iff_left (q.slope * t)).mp (by
      simpa only [Line.eval, add_mul, add_assoc] using htarget)
  have hstrict : S * t + H < q.height := (lt_sub_iff_add_lt).mp (by
    simpa only [D, Line.eval, mul_zero, zero_add] using hst)
  exact hstrict.not_ge hheight'

/-- For a finite affine family, open-ray and closed-ray domination are equivalent. -/
theorem le_envelope_pos_iff_nonneg {ι : Type*} (first : ι) (rest : List ι)
    (L : ι → Line K) (q : Line K) :
    (∀ t : K, 0 < t → q.eval t ≤ envelope first rest L t) ↔
      (∀ t : K, 0 ≤ t → q.eval t ≤ envelope first rest L t) := by
  constructor
  · intro h t ht
    rcases eq_or_lt_of_le ht with rfl | ht
    · exact le_envelope_zero_of_pos first rest L q h
    · exact h t ht
  · exact fun h t ht ↦ h t ht.le

#print axioms maxFrom_le
#print axioms le_envelope_zero_of_pos
#print axioms le_envelope_pos_iff_nonneg

end Delta3.WeightedEnvelope
