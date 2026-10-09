import ErdosSzekeres.Omission.Domains
import ErdosSzekeres.Suk.HorizontalCounting

namespace ErdosSzekeres.Omission

open ActualRanks BalancedCatalog

/-- Ordered real points, with general position expressed by nonzero determinants. -/
structure Configuration (n : ℕ) where
  point : Fin n → Point
  xOrder : StrictMono (fun i => point i 0)
  generalPosition : ∀ i j k : Fin n, i < j → j < k →
    orient (point i) (point j) (point k) ≠ 0

namespace Configuration

/-- Construct the ordered configuration from the project's usual real-set
general-position predicate. No realizability assumption is added. -/
def ofGeneralPosition {n : ℕ} (p : Fin n → Point)
    (hx : StrictMono (fun i => p i 0))
    (hgp : GeneralPosition (Finset.univ.image p)) : Configuration n where
  point := p
  xOrder := hx
  generalPosition := by
    intro i j k hij hjk
    have hinj : Function.Injective p := fun a b h => hx.injective (congrArg (· 0) h)
    exact (generalPosition_iff_orient_ne_zero _).mp hgp _
      (Finset.mem_image_of_mem p (Finset.mem_univ i)) _
      (Finset.mem_image_of_mem p (Finset.mem_univ j)) _
      (Finset.mem_image_of_mem p (Finset.mem_univ k))
      (hinj.ne hij.ne) (hinj.ne (hij.trans hjk).ne) (hinj.ne hjk.ne)

noncomputable def cup {n : ℕ} (c : Configuration n) (i j k : ℕ) : Bool := by
  classical
  exact if h : i < n ∧ j < n ∧ k < n then
    decide (0 < orient (c.point ⟨i, h.1⟩) (c.point ⟨j, h.2.1⟩)
      (c.point ⟨k, h.2.2⟩)) else false

theorem cup_true_iff {n : ℕ} (c : Configuration n) (i j k : Fin n) :
    c.cup i j k = true ↔ 0 < orient (c.point i) (c.point j) (c.point k) := by
  classical
  simp [cup, i.isLt, j.isLt, k.isLt]

theorem cup_false_iff {n : ℕ} (c : Configuration n) (i j k : Fin n)
    (hij : i < j) (hjk : j < k) :
    c.cup i j k = false ↔ orient (c.point i) (c.point j) (c.point k) < 0 := by
  rw [Bool.eq_false_iff]
  change (¬ c.cup i j k = true) ↔ _
  rw [c.cup_true_iff i j k]
  have hn := c.generalPosition i j k hij hjk
  constructor
  · intro h
    exact lt_of_le_of_ne (le_of_not_gt h) hn
  · intro h
    exact not_lt.mpr h.le

/-- A genuine k-cup: every increasing triple of the selected real points
has positive orientation. -/
def HasCup {n : ℕ} (c : Configuration n) (k : ℕ) : Prop :=
  ∃ f : Fin k → Fin n, StrictMono f ∧
    ∀ i j l, i < j → j < l → 0 < orient (c.point (f i)) (c.point (f j)) (c.point (f l))

/-- A genuine k-cap, with negative orientation on every increasing triple. -/
def HasCap {n : ℕ} (c : Configuration n) (k : ℕ) : Prop :=
  ∃ f : Fin k → Fin n, StrictMono f ∧
    ∀ i j l, i < j → j < l → orient (c.point (f i)) (c.point (f j)) (c.point (f l)) < 0

private theorem chain3_getElem {α : Type*} {R : α → α → α → Prop}
    {xs : List α} (h : xs.Chain3' R) (i : ℕ) (hi : i + 2 < xs.length) :
    R xs[i] xs[i + 1] xs[i + 2] := by
  induction i generalizing xs with
  | zero =>
    obtain ⟨a, b, c, xs, rfl⟩ := List.takeHead3 (show 3 ≤ xs.length by omega)
    exact (List.chain3'_cons.mp h).1
  | succ i ih =>
    cases xs with
    | nil => simp at hi
    | cons a xs =>
      have hi' : i + 2 < xs.length := by simp only [List.length_cons] at hi; omega
      simpa [Nat.add_assoc] using ih h.tail hi'

/-- An attained ending path consists of actual, distinct indices in the same
finite configuration, rather than merely numerical upper bounds on ranks. -/
theorem endingPath_embedding {n u v k : ℕ} {color : Bool} (c : Configuration n)
    (path : EndingPath c.cup color u v k) (hvn : v < n) :
    ∃ f : Fin k → Fin n, StrictMono f ∧ ∀ i (hi : i + 2 < k),
      c.cup (f ⟨i, by omega⟩) (f ⟨i + 1, by omega⟩) (f ⟨i + 2, hi⟩) = color := by
  obtain ⟨xs, len, chain, bounded⟩ := list_witness path
  let ys := xs ++ [u, v]
  let f : Fin k → Fin n := fun i =>
    ⟨ys.get ⟨i.val, by dsimp [ys]; omega⟩,
      lt_of_le_of_lt (bounded _ (ys.get_mem _)) hvn⟩
  refine ⟨f, ?_, ?_⟩
  · intro i j hij
    exact List.Sorted.rel_get_of_lt chain.1.pairwise hij
  · intro i hi
    exact chain3_getElem chain.2 i (by omega)

theorem endingPath_hasCup {n u v k : ℕ} (c : Configuration n)
    (path : EndingPath c.cup true u v k) (hvn : v < n) : c.HasCup k := by
  obtain ⟨f, hf, hpath⟩ := c.endingPath_embedding path hvn
  refine ⟨f, hf, ?_⟩
  apply Suk.transitive_path_clique _
    (Suk.horizontal_positive_transitive (fun i => c.point (f i)) (c.xOrder.comp hf))
  intro i hi
  exact (c.cup_true_iff _ _ _).mp (hpath i hi)

theorem endingPath_hasCap {n u v k : ℕ} (c : Configuration n)
    (path : EndingPath c.cup false u v k) (hvn : v < n) : c.HasCap k := by
  obtain ⟨f, hf, hpath⟩ := c.endingPath_embedding path hvn
  have nonpositive := Suk.transitive_path_clique
    (fun i j l => ¬ 0 < orient (c.point (f i)) (c.point (f j)) (c.point (f l)))
    (Suk.horizontal_nonpositive_transitive (fun i => c.point (f i)) (c.xOrder.comp hf))
    (fun i hi => not_lt.mpr (le_of_lt ((c.cup_false_iff _ _ _
      (hf (by change i < i + 1; omega))
      (hf (by change i + 1 < i + 2; omega))).mp (hpath i hi))))
  refine ⟨f, hf, ?_⟩
  intro i j l hij hjl
  have hn := c.generalPosition (f i) (f j) (f l) (hf hij) (hf hjl)
  have h := nonpositive i j l hij hjl
  exact lt_of_le_of_ne (le_of_not_gt h) hn

theorem avoids_of_noCup {n k : ℕ} (c : Configuration n) (h : ¬ c.HasCup k) :
    Avoids n c.cup true k :=
  fun _ _ hv path => h (c.endingPath_hasCup path hv)

theorem avoids_of_noCap {n k : ℕ} (c : Configuration n) (h : ¬ c.HasCap k) :
    Avoids n c.cup false k :=
  fun _ _ hv path => h (c.endingPath_hasCap path hv)

/-- The actual point-to-catalog assignment, retaining the exact 252-state order
used by the checked balanced certificate. -/
noncomputable def balancedOwner {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7) : Fin n → Fin 252 :=
  ownerIndex n c.cup (c.avoids_of_noCap noCap) (c.avoids_of_noCup noCup)

theorem balancedOwner_injective {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7) :
    Function.Injective (c.balancedOwner noCap noCup) :=
  ownerIndex_injective n c.cup (c.avoids_of_noCap noCap) (c.avoids_of_noCup noCup)

/-- The classical 252-state population bound follows from the proved geometric
encoding. No octagon row constraints, or improved geometric bound, are assumed. -/
theorem balanced_universe_bound {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 7) (noCup : ¬ c.HasCup 7) : n ≤ 252 := by
  simpa using Fintype.card_le_of_injective _ (c.balancedOwner_injective noCap noCup)

end Configuration
end ErdosSzekeres.Omission
