import FieldAdapter

/-! Finite two-support necessity for affine domination on the nonnegative ray. -/

namespace Delta3.WeightedEnvelope

variable {K : Type*} [LinearOrder K]

/-- A nonempty eligible part of a finite list has a maximizing member. -/
theorem exists_max_on {ι : Type*} (s : List ι) (P : ι → Prop) (f : ι → K)
    (h : ∃ i ∈ s, P i) : ∃ i ∈ s, P i ∧ ∀ j ∈ s, P j → f j ≤ f i := by
  induction s with
  | nil => exact h.elim fun _ hi ↦ False.elim (List.not_mem_nil hi.1)
  | cons a s ih =>
    by_cases ht : ∃ i ∈ s, P i
    · obtain ⟨m, hm, hPm, hmax⟩ := ih ht
      by_cases ha : P a ∧ f m ≤ f a
      · exact ⟨a, .head s, ha.1, fun j hj hP ↦ (List.mem_cons.mp hj).elim
          (fun hja ↦ (congrArg f hja).le) (fun hjs ↦ (hmax j hjs hP).trans ha.2)⟩
      · refine ⟨m, .tail a hm, hPm, ?_⟩
        exact fun j hj hP ↦ (List.mem_cons.mp hj).elim
          (fun hja ↦ (congrArg f hja).le.trans
            (lt_of_not_ge (fun hma ↦ ha ⟨hja ▸ hP, hma⟩)).le)
          (fun hjs ↦ hmax j hjs hP)
    · have ha : P a := h.elim fun i hi ↦ (List.mem_cons.mp hi.1).elim
        (fun hia ↦ hia ▸ hi.2) (fun his ↦ False.elim (ht ⟨i, his, hi.2⟩))
      exact ⟨a, .head s, ha, fun j hj hP ↦ (List.mem_cons.mp hj).elim
        (fun hja ↦ (congrArg f hja).le) (fun hjs ↦ False.elim (ht ⟨j, hjs, hP⟩))⟩

/-- The corresponding minimizing member, obtained by reversing the order. -/
theorem exists_min_on {ι : Type*} (s : List ι) (P : ι → Prop) (f : ι → K)
    (h : ∃ i ∈ s, P i) : ∃ i ∈ s, P i ∧ ∀ j ∈ s, P j → f i ≤ f j :=
  exists_max_on (K := Kᵒᵈ) s P f h

variable [Field K] [IsStrictOrderedRing K]

local instance : Lean.Grind.Field K := grindField K

theorem eval_neg_iff_above_root {d : K} (e t : K) (hd : d < 0) :
    d * t + e < 0 ↔ e / (-d) < t := by
  rw [div_lt_iff₀ (neg_pos.mpr hd)]
  simp only [mul_neg, mul_comm t d]
  grind

theorem eval_neg_iff_below_root {d : K} (e t : K) (hd : 0 < d) :
    d * t + e < 0 ↔ t < (-e) / d := by
  rw [lt_div_iff₀ hd, mul_comm t d]
  grind

theorem midpoint_bounds {a b : K} (h : a < b) : a < (a + b) / 2 ∧ (a + b) / 2 < b :=
  ⟨(lt_div_iff₀ (show (0 : K) < 2 from zero_lt_two)).2
      ((mul_two a).trans_lt (add_lt_add_left h a)),
    (div_lt_iff₀ (show (0 : K) < 2 from zero_lt_two)).2
      ((add_lt_add_right h b).trans_eq (mul_two b).symm)⟩

/-- After subtracting the target, absence of a single certificate forces a straddling pair. -/
theorem two_residual_of_no_single {ι : Type*} (s : List ι) (d e : ι → K)
    (hdom : ∀ t : K, 0 ≤ t → ∃ i ∈ s, 0 ≤ d i * t + e i)
    (hno : ∀ i ∈ s, 0 ≤ d i → e i < 0) :
    ∃ i ∈ s, ∃ j ∈ s, d i < 0 ∧ 0 < d j ∧ d i * e j ≤ d j * e i := by
  obtain ⟨i0, hi0, he0⟩ := hdom 0 (le_refl 0)
  have he0' : 0 ≤ e i0 := by simpa only [mul_zero, zero_add] using he0
  have hd0 : d i0 < 0 := lt_of_not_ge fun hdi ↦ (not_lt_of_ge he0') (hno i0 hi0 hdi)
  obtain ⟨i, hi, hdi, hmax⟩ :=
    exists_max_on s (fun i ↦ d i < 0) (fun i ↦ e i / (-d i)) ⟨i0, hi0, hd0⟩
  have hA0 : 0 ≤ e i / (-d i) :=
    (div_nonneg he0' (neg_nonneg.mpr hd0.le)).trans (hmax i0 hi0 hd0)
  have hlow : ∀ k ∈ s, d k ≤ 0 → ∀ t : K, e i / (-d i) < t → d k * t + e k < 0 :=
    fun k hk hdk t ht ↦ (lt_or_eq_of_le hdk).elim
      (fun hd ↦ (eval_neg_iff_above_root (e k) t hd).2 ((hmax k hk hd).trans_lt ht))
      (fun hd ↦ by simpa only [hd, zero_mul, zero_add] using hno k hk hd.ge)
  obtain ⟨k, hk, hkvalue⟩ := hdom (e i / (-d i) + 1) (add_nonneg hA0 zero_le_one)
  have hdk : 0 < d k := lt_of_not_ge fun hd ↦
    (not_lt_of_ge hkvalue) (hlow k hk hd _ (lt_add_of_pos_right _ zero_lt_one))
  obtain ⟨j, hj, hdj, hmin⟩ :=
    exists_min_on s (fun j ↦ 0 < d j) (fun j ↦ (-e j) / d j) ⟨k, hk, hdk⟩
  have hBA : (-e j) / d j ≤ e i / (-d i) := le_of_not_gt fun hAB ↦ by
    have hmid := midpoint_bounds hAB
    obtain ⟨r, hr, hrvalue⟩ :=
      hdom ((e i / (-d i) + (-e j) / d j) / 2) (hA0.trans hmid.1.le)
    exact (not_lt_of_ge hrvalue) ((le_or_gt (d r) 0).elim
      (fun hd ↦ hlow r hr hd _ hmid.1)
      (fun hd ↦ (eval_neg_iff_below_root (e r) _ hd).2
        (hmid.2.trans_le (hmin r hr hd))))
  have hcross := (div_le_div_iff₀ hdj (neg_pos.mpr hdi)).mp hBA
  exact ⟨i, hi, j, hj, hdi, hdj, by
    simpa only [neg_mul, mul_neg, neg_neg, mul_comm] using hcross⟩

/-- The explicit convex weight for a pair straddling residual slope zero. -/
theorem residual_pair_certificate {a b x y : K} (ha : a < 0) (hb : 0 < b)
    (hcross : a * y ≤ b * x) :
    ∃ w : K, 0 < w ∧ w < 1 ∧ w * a + (1 - w) * b = 0 ∧ 0 ≤ w * x + (1 - w) * y := by
  have hden : 0 < b - a := sub_pos.mpr (ha.trans hb)
  have hid : b / (b - a) * x + (1 - b / (b - a)) * y = (b * x - a * y) / (b - a) := by
    grind
  have hslope : b / (b - a) * a + (1 - b / (b - a)) * b = 0 := by grind
  have hw : b / (b - a) < 1 := (div_lt_iff₀ hden).2 (by grind)
  exact ⟨b / (b - a), div_pos hb hden, hw, hslope,
    (div_nonneg (sub_nonneg.mpr hcross) hden.le).trans_eq hid.symm⟩

omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem weighted_sub (w a b c : K) :
    w * (a - c) + (1 - w) * (b - c) = w * a + (1 - w) * b - c := by
  grind

/-- If no single line dominates both coefficients, two strictly straddling supports suffice. -/
theorem two_supports_of_no_single {ι : Type*} (s : List ι) (L : ι → Line K) (q : Line K)
    (hdom : ∀ t : K, 0 ≤ t → ∃ i ∈ s, q.eval t ≤ (L i).eval t)
    (hsingle : ¬∃ i ∈ s, q.slope ≤ (L i).slope ∧ q.height ≤ (L i).height) :
    ∃ i ∈ s, ∃ j ∈ s, ∃ w : K,
      (L i).slope < q.slope ∧ q.slope < (L j).slope ∧ 0 < w ∧ w < 1 ∧
      q.slope = w * (L i).slope + (1 - w) * (L j).slope ∧
      q.height ≤ w * (L i).height + (1 - w) * (L j).height := by
  have hno : ∀ i ∈ s, 0 ≤ (L i).slope - q.slope → (L i).height - q.height < 0 :=
    fun i hi hs ↦ sub_neg.mpr (lt_of_not_ge fun hh ↦
      hsingle ⟨i, hi, sub_nonneg.mp hs, hh⟩)
  have hres : ∀ t : K, 0 ≤ t →
      ∃ i ∈ s, 0 ≤ ((L i).slope - q.slope) * t + ((L i).height - q.height) :=
    fun t ht ↦ (hdom t ht).elim fun i hi ↦ ⟨i, hi.1, by
      simpa only [Line.eval, sub_mul, sub_add_sub_comm] using sub_nonneg.mpr hi.2⟩
  obtain ⟨i, hi, j, hj, hdi, hdj, hcross⟩ := two_residual_of_no_single s
    (fun i ↦ (L i).slope - q.slope) (fun i ↦ (L i).height - q.height) hres hno
  obtain ⟨w, hw0, hw1, hws, hwh⟩ := residual_pair_certificate hdi hdj hcross
  exact ⟨i, hi, j, hj, w, sub_neg.mp hdi, sub_pos.mp hdj, hw0, hw1,
    (sub_eq_zero.mp ((weighted_sub w _ _ _).symm.trans hws)).symm,
    sub_nonneg.mp (hwh.trans_eq (weighted_sub w _ _ _))⟩

/-- Universal pointwise domination by a finite family admits at most two support indices.
The repeated-index, weight-one case represents a single support. -/
theorem exists_two_supports_of_pointwise {ι : Type*} (s : List ι) (L : ι → Line K)
    (q : Line K) (hdom : ∀ t : K, 0 ≤ t → ∃ i ∈ s, q.eval t ≤ (L i).eval t) :
    ∃ i ∈ s, ∃ j ∈ s, ∃ w : K, 0 ≤ w ∧ w ≤ 1 ∧
      q.slope ≤ w * (L i).slope + (1 - w) * (L j).slope ∧
      q.height ≤ w * (L i).height + (1 - w) * (L j).height :=
  (Classical.em (∃ i ∈ s, q.slope ≤ (L i).slope ∧ q.height ≤ (L i).height)).elim
    (fun ⟨i, hi, hs, hh⟩ ↦ ⟨i, hi, i, hi, 1, zero_le_one, le_refl 1,
      by simpa only [one_mul, sub_self, zero_mul, add_zero] using hs,
      by simpa only [one_mul, sub_self, zero_mul, add_zero] using hh⟩)
    (fun h ↦ match two_supports_of_no_single s L q hdom h with
      | ⟨i, hi, j, hj, w, _, _, hw0, hw1, hs, hh⟩ =>
        ⟨i, hi, j, hj, w, hw0.le, hw1.le, hs.le, hh⟩)

omit [Field K] [IsStrictOrderedRing K] in
theorem exists_mem_of_le_maxFrom {ι : Type*} (first : ι) (rest : List ι) (f : ι → K)
    (x : K) (h : x ≤ maxFrom (f first) rest f) : ∃ i ∈ first :: rest, x ≤ f i :=
  List.recOn (motive := fun rest ↦ x ≤ maxFrom (f first) rest f →
      ∃ i ∈ first :: rest, x ≤ f i) rest
    (fun h ↦ ⟨first, .head [], h⟩)
    (fun a tail ih h ↦ (le_max_iff.mp h).elim
      (fun ha ↦ ⟨a, .tail first (.head tail), ha⟩)
      (fun ht ↦ (ih ht).elim fun i hi ↦ ⟨i,
        (List.mem_cons.mp hi.1).elim
          (fun heq ↦ List.mem_cons.mpr (Or.inl heq))
          (fun his ↦ .tail first (.tail a his)), hi.2⟩)) h

/-- A finite envelope dominating the target on `t ≥ 0` has a one- or two-support certificate. -/
theorem exists_two_supports_of_le_envelope {ι : Type*} (first : ι) (rest : List ι)
    (L : ι → Line K) (q : Line K)
    (h : ∀ t : K, 0 ≤ t → q.eval t ≤ envelope first rest L t) :
    ∃ i ∈ first :: rest, ∃ j ∈ first :: rest, ∃ w : K, 0 ≤ w ∧ w ≤ 1 ∧
      q.slope ≤ w * (L i).slope + (1 - w) * (L j).slope ∧
      q.height ≤ w * (L i).height + (1 - w) * (L j).height :=
  exists_two_supports_of_pointwise (first :: rest) L q fun t ht ↦
    exists_mem_of_le_maxFrom first rest (fun i ↦ (L i).eval t) (q.eval t) (h t ht)

/-- A two-line coefficient certificate bounds the target by the pair's maximum. -/
theorem le_max_of_two_supports (a b q : Line K) (w : K) (hw0 : 0 ≤ w) (hw1 : w ≤ 1)
    (hs : q.slope ≤ w * a.slope + (1 - w) * b.slope)
    (hh : q.height ≤ w * a.height + (1 - w) * b.height) {t : K} (ht : 0 ≤ t) :
    q.eval t ≤ max (a.eval t) (b.eval t) := by
  calc
    q.eval t ≤ (w * a.slope + (1 - w) * b.slope) * t +
        (w * a.height + (1 - w) * b.height) :=
      add_le_add (mul_le_mul_of_nonneg_right hs ht) hh
    _ = w * a.eval t + (1 - w) * b.eval t := by grind [Line.eval]
    _ ≤ w * max (a.eval t) (b.eval t) + (1 - w) * max (a.eval t) (b.eval t) :=
      add_le_add (mul_le_mul_of_nonneg_left (le_max_left _ _) hw0)
        (mul_le_mul_of_nonneg_left (le_max_right _ _) (sub_nonneg.mpr hw1))
    _ = max (a.eval t) (b.eval t) := by grind

/-- Domination on the entire nonnegative ray is equivalent to a two-support certificate. -/
theorem le_envelope_iff_two_supports {ι : Type*} (first : ι) (rest : List ι)
    (L : ι → Line K) (q : Line K) :
    (∀ t : K, 0 ≤ t → q.eval t ≤ envelope first rest L t) ↔
      ∃ i ∈ first :: rest, ∃ j ∈ first :: rest, ∃ w : K, 0 ≤ w ∧ w ≤ 1 ∧
        q.slope ≤ w * (L i).slope + (1 - w) * (L j).slope ∧
        q.height ≤ w * (L i).height + (1 - w) * (L j).height :=
  ⟨exists_two_supports_of_le_envelope first rest L q,
    fun ⟨i, hi, j, hj, w, hw0, hw1, hs, hh⟩ t ht ↦
      (le_max_of_two_supports (L i) (L j) q w hw0 hw1 hs hh ht).trans
        (max_le (eval_le_envelope first rest L t i hi)
          (eval_le_envelope first rest L t j hj))⟩

#print axioms exists_max_on
#print axioms exists_min_on
#print axioms eval_neg_iff_above_root
#print axioms eval_neg_iff_below_root
#print axioms midpoint_bounds
#print axioms two_residual_of_no_single
#print axioms residual_pair_certificate
#print axioms weighted_sub
#print axioms two_supports_of_no_single
#print axioms exists_two_supports_of_pointwise
#print axioms exists_mem_of_le_maxFrom
#print axioms exists_two_supports_of_le_envelope
#print axioms le_max_of_two_supports
#print axioms le_envelope_iff_two_supports

end Delta3.WeightedEnvelope
