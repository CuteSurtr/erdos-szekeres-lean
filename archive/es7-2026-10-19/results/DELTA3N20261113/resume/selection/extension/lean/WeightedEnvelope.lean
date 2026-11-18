import Mathlib.Algebra.Order.Field.Defs

/-!
# Finite weighted affine-envelope certificates

Finite families are represented by lists to keep imports within the resource budget.
Repeated indices are permitted. No geometric realization or Delta-selection statement is made.
-/

namespace Delta3.WeightedEnvelope

variable {K : Type*} [Field K]

/-- An affine line represented by slope and height at parameter zero. -/
structure Line (K : Type*) where
  slope : K
  height : K

def Line.eval (L : Line K) (t : K) : K := L.slope * t + L.height

/-- A finite indexed sum, including multiplicities. -/
def total {ι : Type*} (s : List ι) (f : ι → K) : K :=
  match s with
  | [] => 0
  | i :: rest => f i + total rest f

theorem total_add {ι : Type*} (s : List ι) (f g : ι → K) :
    total s (fun i ↦ f i + g i) = total s f + total s g := by
  induction s with
  | nil => exact (zero_add 0).symm
  | cons i s ih => simp only [total, ih, add_add_add_comm]

theorem total_mul_right {ι : Type*} (s : List ι) (f : ι → K) (c : K) :
    total s (fun i ↦ f i * c) = total s f * c :=
  List.recOn s (zero_mul c).symm fun i rest ih ↦
    (congrArg (fun x ↦ f i * c + x) ih).trans (add_mul (f i) (total rest f) c).symm

theorem total_weighted_eval {ι : Type*} (s : List ι) (L : ι → Line K) (w : ι → K)
    (t : K) : total s (fun i ↦ w i * (L i).eval t) =
      total s (fun i ↦ w i * (L i).slope) * t + total s (fun i ↦ w i * (L i).height) := by
  simp only [Line.eval, mul_add, ← mul_assoc, total_add, total_mul_right]

variable [LinearOrder K] [IsStrictOrderedRing K]

theorem total_le_total {ι : Type*} (s : List ι) (f g : ι → K)
    (h : ∀ i ∈ s, f i ≤ g i) : total s f ≤ total s g :=
  List.recOn (motive := fun s ↦ (∀ i ∈ s, f i ≤ g i) → total s f ≤ total s g) s
    (fun _ ↦ le_refl 0)
    (fun i rest ih h ↦ add_le_add (h i (.head rest)) (ih fun j hj ↦ h j (.tail i hj))) h

/-- A convex coefficient certificate places the target below any common support upper bound. -/
theorem le_upper_of_weighted_certificate {ι : Type*} (s : List ι) (L : ι → Line K)
    (q : Line K) (w : ι → K) (hw : ∀ i ∈ s, 0 ≤ w i) (hunit : total s w = 1)
    (hslope : q.slope ≤ total s (fun i ↦ w i * (L i).slope))
    (hheight : q.height ≤ total s (fun i ↦ w i * (L i).height))
    {t M : K} (ht : 0 ≤ t) (hM : ∀ i ∈ s, (L i).eval t ≤ M) : q.eval t ≤ M :=
  calc
    q.eval t ≤ total s (fun i ↦ w i * (L i).slope) * t +
        total s (fun i ↦ w i * (L i).height) :=
      add_le_add (mul_le_mul_of_nonneg_right hslope ht) hheight
    _ = total s (fun i ↦ w i * (L i).eval t) := (total_weighted_eval s L w t).symm
    _ ≤ total s (fun i ↦ w i * M) :=
      total_le_total s _ _ fun i hi ↦ mul_le_mul_of_nonneg_left (hM i hi) (hw i hi)
    _ = M := (total_mul_right s w M).trans ((congrArg (fun x ↦ x * M) hunit).trans
      (one_mul M))

/-- Maximum of the listed values together with a base value. -/
def maxFrom {ι : Type*} (base : K) (s : List ι) (f : ι → K) : K :=
  match s with
  | [] => base
  | i :: rest => max (f i) (maxFrom base rest f)

omit [Field K] [IsStrictOrderedRing K] in
theorem le_maxFrom_base {ι : Type*} (base : K) (s : List ι) (f : ι → K) :
    base ≤ maxFrom base s f :=
  List.recOn s (le_refl base) fun _ _ ih ↦ ih.trans (le_max_right _ _)

omit [Field K] [IsStrictOrderedRing K] in
theorem le_maxFrom_of_mem {ι : Type*} (base : K) (s : List ι) (f : ι → K) :
    ∀ i ∈ s, f i ≤ maxFrom base s f :=
  List.recOn (motive := fun s ↦ ∀ i ∈ s, f i ≤ maxFrom base s f) s
    (fun _ hi ↦ nomatch hi)
    (fun _ _ ih i hi ↦ (List.mem_cons.mp hi).elim
      (fun hij ↦ (congrArg f hij).le.trans (le_max_left _ _))
      (fun his ↦ (ih i his).trans (le_max_right _ _)))

/-- The maximum of the nonempty finite family indexed by `first :: rest`. -/
def envelope {ι : Type*} (first : ι) (rest : List ι) (L : ι → Line K) (t : K) : K :=
  maxFrom ((L first).eval t) rest (fun i ↦ (L i).eval t)

omit [IsStrictOrderedRing K] in
theorem eval_le_envelope {ι : Type*} (first : ι) (rest : List ι) (L : ι → Line K)
    (t : K) (i : ι) (hi : i ∈ first :: rest) : (L i).eval t ≤ envelope first rest L t :=
  (List.mem_cons.mp hi).elim
    (fun h ↦ (congrArg (fun j ↦ (L j).eval t) h).le.trans (le_maxFrom_base _ _ _))
    (fun h ↦ le_maxFrom_of_mem ((L first).eval t) rest (fun j ↦ (L j).eval t) i h)

/-- Nonnegative weights with unit sum and dominating slope and height certify the whole ray. -/
theorem le_envelope_of_weighted_certificate {ι : Type*} (first : ι) (rest : List ι)
    (L : ι → Line K) (q : Line K) (w : ι → K)
    (hw : ∀ i ∈ first :: rest, 0 ≤ w i) (hunit : total (first :: rest) w = 1)
    (hslope : q.slope ≤ total (first :: rest) (fun i ↦ w i * (L i).slope))
    (hheight : q.height ≤ total (first :: rest) (fun i ↦ w i * (L i).height))
    {t : K} (ht : 0 ≤ t) : q.eval t ≤ envelope first rest L t :=
  le_upper_of_weighted_certificate _ L q w hw hunit hslope hheight ht
    (eval_le_envelope first rest L t)

#print axioms total_add
#print axioms total_mul_right
#print axioms total_weighted_eval
#print axioms total_le_total
#print axioms le_upper_of_weighted_certificate
#print axioms le_maxFrom_base
#print axioms le_maxFrom_of_mem
#print axioms eval_le_envelope
#print axioms le_envelope_of_weighted_certificate

end Delta3.WeightedEnvelope
