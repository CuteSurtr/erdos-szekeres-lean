/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, formal/sources/ES8ActualRanks.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Catalog data: CC BY 4.0; see docs/THIRD_PARTY.md.
Changes: local namespaces/imports, Lean/Mathlib 4.24 compatibility, kernel-only checks.
-/
import ErdosSzekeres.Omission.StateInterface
import Mathlib.Data.Finset.Max
import Mathlib.Tactic
import ErdosSzekeres.Vendor.ETV.Config.Lemmas

namespace ErdosSzekeres.Omission.ActualRanks

/-- An attained monotone path ending at the exact ordered pair. Each constructor
adds one actual, strictly later vertex and checks the actual triple color. -/
inductive EndingPath (cup : Nat → Nat → Nat → Bool) (color : Bool) : Nat → Nat → Nat → Prop
  | pair {u v : Nat} : u < v → EndingPath cup color u v 2
  | step {t u v l : Nat} : EndingPath cup color t u l → u < v → cup t u v = color →
      EndingPath cup color u v (l+1)

theorem length_bounds {cup : Nat → Nat → Nat → Bool} {color : Bool} {u v l : Nat}
    (path : EndingPath cup color u v l) : 2 ≤ l ∧ l ≤ v+1 ∧ u < v := by
  induction path with
  | pair h => omega
  | step _ h _ ih => omega

def colorConfig (cup : Nat → Nat → Nat → Bool) (color : Bool) : Config Nat where
  Cup3 := fun a b c => cup a b c = color
  DecidableCup3 := inferInstance

/-- The inductive witness is a concrete strictly ordered list with the specified
length and exact final pair. Every vertex belongs to the same ambient prefix. -/
theorem list_witness {cup : Nat → Nat → Nat → Bool} {color : Bool} {u v l : Nat}
    (path : EndingPath cup color u v l) :
    ∃ xs : List Nat, (xs ++ [u,v]).length=l ∧
      (colorConfig cup color).Cup (xs ++ [u,v]) ∧
      ∀ a ∈ xs ++ [u,v], a ≤ v := by
  induction path with
  | @pair u v h =>
    refine ⟨[],by simp,by simpa using h,?_⟩
    intro a ha
    simp at ha
    rcases ha with rfl | rfl <;> omega
  | @step t u v l path huv same ih =>
    obtain ⟨xs,len,chain,bounded⟩ := ih
    refine ⟨xs ++ [t],?_,?_,?_⟩
    · simp only [List.length_append,List.length_cons,List.length_nil] at *
      omega
    · have triple : (colorConfig cup color).Cup3 t u v := same
      have next : (colorConfig cup color).Cup [u,v] := Config.Cup.pair.mpr huv
      have joined := Config.Cup.append_cons3.mpr ⟨chain,triple,next⟩
      simpa only [List.append_assoc,List.cons_append,List.nil_append] using joined
    · intro a ha
      have whole : (xs ++ [t]) ++ [u,v] = (xs ++ [t,u]) ++ [v] := by simp
      rw [whole,List.mem_append] at ha
      rcases ha with old | last
      · have := bounded a old
        omega
      · have : a=v := by simpa using last
        omega


noncomputable def lengths (cup : Nat → Nat → Nat → Bool) (color : Bool) (u v : Nat) : Finset Nat :=
  by classical exact (Finset.range (v+2)).filter (EndingPath cup color u v)

theorem mem_lengths {cup : Nat → Nat → Nat → Bool} {color : Bool} {u v l : Nat} :
    l ∈ lengths cup color u v ↔ EndingPath cup color u v l := by
  classical
  simp only [lengths,Finset.mem_filter,Finset.mem_range]
  constructor
  · exact And.right
  · intro h
    exact ⟨by have := length_bounds h; omega,h⟩

theorem lengths_nonempty (cup : Nat → Nat → Nat → Bool) (color : Bool) (u v : Nat)
    (huv : u < v) : (lengths cup color u v).Nonempty :=
  ⟨2,mem_lengths.mpr (.pair huv)⟩

noncomputable def rank (cup : Nat → Nat → Nat → Bool) (color : Bool) (u v : Nat) : Nat :=
  if h : u < v then (lengths cup color u v).max' (lengths_nonempty cup color u v h) else 0

theorem rank_attained (cup : Nat → Nat → Nat → Bool) (color : Bool) (u v : Nat)
    (huv : u < v) : EndingPath cup color u v (rank cup color u v) := by
  classical
  unfold rank
  rw [dif_pos huv]
  exact mem_lengths.mp (Finset.max'_mem _ _)

theorem rank_ge {cup : Nat → Nat → Nat → Bool} {color : Bool} {u v l : Nat}
    (path : EndingPath cup color u v l) : l ≤ rank cup color u v := by
  classical
  have huv := (length_bounds path).2.2
  unfold rank
  rw [dif_pos huv]
  exact Finset.le_max' _ _ (mem_lengths.mpr path)

theorem rank_growth (cup : Nat → Nat → Nat → Bool) (color : Bool) (t u v : Nat)
    (htu : t < u) (huv : u < v) (same : cup t u v = color) :
    rank cup color t u < rank cup color u v := by
  have h := rank_ge (EndingPath.step (rank_attained cup color t u htu) huv same)
  omega

noncomputable def labels (cup : Nat → Nat → Nat → Bool) (u v : Nat) : ErdosSzekeres.Omission.StateInterface.Label :=
  (rank cup false u v - 1, rank cup true u v - 1)

/-- Actual maxima, not unsupported upper rank labels, satisfy the growth interface. -/
theorem labels_increasing (n : Nat) (cup : Nat → Nat → Nat → Bool) :
    ErdosSzekeres.Omission.StateInterface.IncreasingLabels n cup (labels cup) := by
  intro u v w huv hvw _
  constructor
  · intro color
    have growth := rank_growth cup false u v w huv hvw color
    have low := (length_bounds (rank_attained cup false u v huv)).1
    simp only [labels]
    omega
  · intro color
    have growth := rank_growth cup true u v w huv hvw color
    have low := (length_bounds (rank_attained cup true u v huv)).1
    simp only [labels]
    omega

theorem actual_incoming_admissible (n : Nat) (cup : Nat → Nat → Nat → Bool) :
    ErdosSzekeres.Omission.StateInterface.AdmissibleStates n (labels cup) (ErdosSzekeres.Omission.StateInterface.Incoming (labels cup)) :=
  ErdosSzekeres.Omission.StateInterface.incoming_admissible n cup (labels cup) (labels_increasing n cup)

/-- Every shorter length is attained by a prefix of the same inductively built
path; its ending vertex is no later than the original ending vertex. -/
theorem shorter_path {cup : Nat → Nat → Nat → Bool} {color : Bool} {u v l : Nat}
    (path : EndingPath cup color u v l) (m : Nat) (two : 2 ≤ m) (small : m ≤ l) :
    ∃ a b, b ≤ v ∧ EndingPath cup color a b m := by
  induction path with
  | @pair u v h =>
    have : m=2 := by omega
    subst m
    exact ⟨u,v,le_rfl,.pair h⟩
  | @step t u v l path huv color ih =>
    by_cases short : m ≤ l
    · obtain ⟨a,b,hb,hp⟩ := ih short
      exact ⟨a,b,by omega,hp⟩
    · have : m=l+1 := by omega
      subst m
      exact ⟨u,v,le_rfl,.step path huv color⟩

def Avoids (n : Nat) (cup : Nat → Nat → Nat → Bool) (color : Bool) (k : Nat) : Prop :=
  ∀ u v, v < n → ¬ EndingPath cup color u v k

theorem rank_lt_of_avoids (n : Nat) (cup : Nat → Nat → Nat → Bool) (color : Bool)
    (k : Nat) (hk : 2 ≤ k) (avoid : Avoids n cup color k)
    (u v : Nat) (huv : u < v) (hvn : v < n) : rank cup color u v < k := by
  by_contra high
  obtain ⟨a,b,hb,hpath⟩ := shorter_path (rank_attained cup color u v huv) k hk (by omega)
  exact avoid a b (by omega) hpath

/-- The balanced pair labels genuinely lie in the positive five-by-five grid. -/
theorem balanced_label_bounds (n : Nat) (cup : Nat → Nat → Nat → Bool)
    (caps : Avoids n cup false 7) (cups : Avoids n cup true 7)
    (u v : Nat) (huv : u < v) (hvn : v < n) :
    1 ≤ (labels cup u v).1 ∧ (labels cup u v).1 ≤ 5 ∧
    1 ≤ (labels cup u v).2 ∧ (labels cup u v).2 ≤ 5 := by
  have c := rank_lt_of_avoids n cup false 7 (by omega) caps u v huv hvn
  have q := rank_lt_of_avoids n cup true 7 (by omega) cups u v huv hvn
  have cl := (length_bounds (rank_attained cup false u v huv)).1
  have ql := (length_bounds (rank_attained cup true u v huv)).1
  simp only [labels]
  omega


theorem false_cup_iff_cap (cup : Nat → Nat → Nat → Bool) (xs : List Nat) :
    (colorConfig cup false).Cup xs ↔ (colorConfig cup true).Cap xs := by
  have predicates : (colorConfig cup false).Cup3 = (colorConfig cup true).Cap3 := by
    funext a b c
    apply propext
    change cup a b c = false ↔ ¬ cup a b c = true
    cases cup a b c <;> simp
  simp only [Config.Cup,Config.Cap,predicates]

theorem avoids_of_no_cup (n k : Nat) (cup : Nat → Nat → Nat → Bool)
    (noCup : ¬ (colorConfig cup true).HasNCup k (Finset.range n)) :
    Avoids n cup true k := by
  intro u v hv path
  obtain ⟨xs,len,chain,bounded⟩ := list_witness path
  apply noCup
  refine ⟨xs ++ [u,v],⟨chain,len⟩,?_⟩
  intro a ha
  exact Finset.mem_range.mpr (by have := bounded a ha; omega)

theorem avoids_of_no_cap (n k : Nat) (cup : Nat → Nat → Nat → Bool)
    (noCap : ¬ (colorConfig cup true).HasNCap k (Finset.range n)) :
    Avoids n cup false k := by
  intro u v hv path
  obtain ⟨xs,len,chain,bounded⟩ := list_witness path
  apply noCap
  refine ⟨xs ++ [u,v],⟨(false_cup_iff_cap cup _).mp chain,len⟩,?_⟩
  intro a ha
  exact Finset.mem_range.mpr (by have := bounded a ha; omega)


#print axioms actual_incoming_admissible
end ErdosSzekeres.Omission.ActualRanks
