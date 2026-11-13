import ErdosSzekeres.OmissionCertificates

namespace ErdosSzekeres.OmissionCertificates

open scoped BigOperators

/-- Safe table lookup preserves a checked property, including the default value
used outside the table. This lets large row catalogs use small nested arrays. -/
theorem array_all_getElem! {α : Type*} [Inhabited α] (xs : Array α)
    (p : α → Bool) (h : xs.all p = true) (hdefault : p default = true) (i : ℕ) :
    p xs[i]! = true := by
  by_cases hi : i < xs.size
  · simpa only [getElem!_pos xs i hi] using (Array.all_eq_true.mp h i hi)
  · simpa only [getElem!_neg xs i hi] using hdefault

/-- Pack a bounded coefficient vector into one natural number. -/
def pack {n : ℕ} (base : ℕ) (coefficient : Fin n → ℕ) : ℕ :=
  ∑ i, coefficient i * base ^ i.val

theorem pack_succ {n : ℕ} (base : ℕ) (coefficient : Fin (n + 1) → ℕ) :
    pack base coefficient = coefficient 0 + base * pack base (fun i => coefficient i.succ) := by
  simp only [pack, Fin.sum_univ_succ, Fin.val_zero, pow_zero, mul_one,
    Fin.val_succ, pow_succ, Finset.mul_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro i _
  ring

/-- Equal packed numbers have equal digits when all coefficients are below the
base. This lets certificate checks aggregate sparse rows with big integers. -/
theorem pack_injective_of_lt {n base : ℕ} (hb : 1 < base)
    {f g : Fin n → ℕ} (hf : ∀ i, f i < base) (hg : ∀ i, g i < base)
    (heq : pack base f = pack base g) : f = g := by
  induction n with
  | zero => funext i; exact Fin.elim0 i
  | succ n ih =>
      rw [pack_succ, pack_succ] at heq
      have hzero : f 0 = g 0 := by
        have hm := congrArg (fun x => x % base) heq
        simpa [Nat.add_mod, Nat.mod_eq_of_lt (hf 0), Nat.mod_eq_of_lt (hg 0)] using hm
      have htail : pack base (fun i => f i.succ) = pack base (fun i => g i.succ) := by
        rw [hzero] at heq
        exact Nat.eq_of_mul_eq_mul_left (by omega) (Nat.add_left_cancel heq)
      have he := ih (fun i => hf i.succ) (fun i => hg i.succ) htail
      funext i
      refine Fin.cases hzero (fun j => ?_) i
      exact congrFun he j

/-- Sparse row encoding: a support contributes one base-power for each state. -/
def rowCode {n : ℕ} (base : ℕ) (support : Finset (Fin n)) : ℕ :=
  ∑ i ∈ support, base ^ i.val

theorem pack_load {n : ℕ} {ρ : Type*} [Fintype ρ] (base : ℕ)
    (support : ρ → Finset (Fin n)) (weight : ρ → ℕ) :
    pack base (load support weight) = ∑ r, weight r * rowCode base (support r) := by
  classical
  simp only [pack, load, rowCode, Finset.sum_mul, Finset.mul_sum, ite_mul, zero_mul]
  rw [Finset.sum_comm]
  congr 1
  funext r
  simp

/-- A packed equality and a no-carry bound certify all column loads at once. -/
theorem load_eq_of_packed {n base : ℕ} {ρ : Type*} [Fintype ρ]
    (support : ρ → Finset (Fin n)) (weight : ρ → ℕ) (coefficients : Fin n → ℕ)
    (hb : 1 < base) (hw : (∑ r, weight r) < base)
    (hc : ∀ i, coefficients i < base)
    (heq : pack base coefficients = ∑ r, weight r * rowCode base (support r)) :
    coefficients = load support weight := by
  apply pack_injective_of_lt hb hc
  · intro i
    apply lt_of_le_of_lt ?_ hw
    unfold load
    apply Finset.sum_le_sum
    intro r _
    split_ifs <;> omega
  · rwa [pack_load]

/-- Horner evaluation avoids computing a separate power for each coefficient. -/
def packList (base : ℕ) : List ℕ → ℕ
  | [] => 0
  | c :: cs => c + base * packList base cs

theorem packList_eq_pack (base : ℕ) (cs : List ℕ) :
    packList base cs = pack base cs.get := by
  induction cs with
  | nil => simp [packList, pack]
  | cons c cs ih =>
      rw [packList, pack_succ]
      simpa using congrArg (fun x => c + base * x) ih

/-- Sparse weighted sums only traverse rows that occur in a leaf. -/
def sparseSum {ρ : Type*} (value : ρ → ℕ) : List (ρ × ℕ) → ℕ
  | [] => 0
  | (r, w) :: entries => w * value r + sparseSum value entries

theorem sparseSum_eq_sum {ρ : Type*} (value : ρ → ℕ) (entries : List (ρ × ℕ)) :
    sparseSum value entries = ∑ i : Fin entries.length,
      (entries.get i).2 * value (entries.get i).1 := by
  induction entries with
  | nil => simp [sparseSum]
  | cons e entries ih =>
      simp only [List.length_cons]
      rw [sparseSum, Fin.sum_univ_succ]
      simpa using congrArg (fun x => e.2 * value e.1 + x) ih

/-- Prechecked row encodings may be shared by every leaf. The concrete check
uses sparse weighted sums and Horner evaluation, while the conclusion gives
the original incidence-matrix column loads. -/
theorem load_eq_of_sparse_packed {ρ : Type*} (base : ℕ) (cs : List ℕ)
    (support : ρ → Finset (Fin cs.length)) (code : ρ → ℕ)
    (entries : List (ρ × ℕ)) (hcode : ∀ r, code r = rowCode base (support r))
    (hb : 1 < base) (hw : sparseSum (fun _ => 1) entries < base)
    (hc : cs.all (fun c => decide (c < base)) = true)
    (heq : packList base cs = sparseSum code entries) :
    cs.get = load (fun i : Fin entries.length => support (entries.get i).1)
      (fun i => (entries.get i).2) := by
  apply load_eq_of_packed (base := base)
  · exact hb
  · simpa [sparseSum_eq_sum] using hw
  · intro i
    exact of_decide_eq_true ((List.all_eq_true.mp hc) _ (List.get_mem cs i))
  · rw [← packList_eq_pack, heq, sparseSum_eq_sum]
    simp only [hcode]

/-- A sparse leaf is enough to contradict a feasible assignment of the full
row catalog. Its stored coefficients are checked independently by the packed
identity above. No enumeration of zero-weight catalog rows is needed. -/
theorem sparse_conditioned_excludes {ι ρ : Type*} [Fintype ι] [DecidableEq ι]
    (support : ρ → Finset ι) (demand : ρ → ℕ) (entries : List (ρ × ℕ))
    (coefficients : ι → ℕ) (missing occupied : Finset ι) (capacity budget : ℕ)
    (hloads : coefficients =
      load (fun i : Fin entries.length => support (entries.get i).1)
        (fun i => (entries.get i).2))
    (hmargin : capacity * (budget - missing.card) +
        ∑ i, (if i ∈ missing ∪ occupied then 0 else coefficients i - capacity) +
        ∑ i ∈ missing, coefficients i < sparseSum demand entries) :
    ¬ ∃ holes : ι → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ budget ∧
      (∀ i ∈ missing, holes i = 1) ∧ (∀ i ∈ occupied, holes i = 0) := by
  rw [hloads, sparseSum_eq_sum] at hmargin
  have h := conditioned_excludes_of_full_load
    (fun i : Fin entries.length => support (entries.get i).1)
    (fun i => demand (entries.get i).1) (fun i => (entries.get i).2)
    missing occupied capacity budget hmargin
  rintro ⟨holes, hbool, hrows, hbudget, hm, hz⟩
  exact h ⟨holes, hbool, fun i => hrows (entries.get i).1, hbudget, hm, hz⟩

/-- A list traversal computes the sum without repeated indexed list access. -/
theorem sum_map_eq_sum_get (f : ℕ → ℕ) (cs : List ℕ) :
    (cs.map f).sum = ∑ i : Fin cs.length, f (cs.get i) := by
  induction cs with
  | nil => simp
  | cons c cs ih =>
      simp only [List.length_cons, List.map_cons, List.sum_cons, Fin.sum_univ_succ]
      simpa only [List.get_cons_zero, List.get_cons_succ] using
        congrArg (fun x => f c + x) ih

/-- The free-column excess can be computed by subtracting the fixed columns
from a single linear traversal of all digits. The inequality is written without
natural subtraction of the two totals, so no underflow side condition is needed. -/
theorem sparse_list_conditioned_excludes {ρ : Type*} (cs : List ℕ)
    (support : ρ → Finset (Fin cs.length)) (demand : ρ → ℕ)
    (entries : List (ρ × ℕ)) (missing occupied : Finset (Fin cs.length))
    (capacity budget : ℕ)
    (hloads : cs.get =
      load (fun i : Fin entries.length => support (entries.get i).1)
        (fun i => (entries.get i).2))
    (hmargin : capacity * (budget - missing.card) +
        (cs.map (fun c => c - capacity)).sum + ∑ i ∈ missing, cs.get i <
      sparseSum demand entries + ∑ i ∈ missing ∪ occupied, (cs.get i - capacity)) :
    ¬ ∃ holes : Fin cs.length → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ budget ∧
      (∀ i ∈ missing, holes i = 1) ∧ (∀ i ∈ occupied, holes i = 0) := by
  apply sparse_conditioned_excludes support demand entries cs.get missing occupied
    capacity budget hloads
  have partition : (cs.map (fun c => c - capacity)).sum =
      (∑ i ∈ missing ∪ occupied, (cs.get i - capacity)) +
        ∑ i, (if i ∈ missing ∪ occupied then 0 else cs.get i - capacity) := by
    rw [sum_map_eq_sum_get]
    rw [Finset.sum_ite]
    simp only [Finset.sum_const_zero, zero_add, Finset.filter_notMem_eq_sdiff]
    simpa only [Finset.univ_inter] using
      (Finset.sum_inter_add_sum_diff Finset.univ (missing ∪ occupied)
        (fun i => cs.get i - capacity)).symm
  rw [partition] at hmargin
  omega

end ErdosSzekeres.OmissionCertificates
