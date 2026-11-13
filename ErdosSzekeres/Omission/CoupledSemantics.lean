import ErdosSzekeres.Omission.BlockGeometry
import ErdosSzekeres.OrientationPackets
import ErdosSzekeres.OrientationObstructions
import ErdosSzekeres.OrientationConvexity
import Mathlib.Tactic.Sat.FromLRAT

/-! Semantics for small coupled residual-state certificates. All atomic
propositions refer to actual owners in one real configuration. -/
namespace ErdosSzekeres.Omission.Coupled
open ResidualRanks ResidualCatalog StateInterface

inductive Atom (k : ℕ)
  | falsum
  | before (i j : Fin k)
  | capGe (i j : Fin k) (threshold : ℕ)
  | cupGe (i j : Fin k) (threshold : ℕ)
  | positive (i j l : Fin k)
  | convex (i j l m : Fin k)
  deriving DecidableEq, Repr

inductive Expr (k : ℕ)
  | constant (value : Bool)
  | atom (a : Atom k) (positive : Bool)
  deriving DecidableEq, Repr

def Expr.neg : Expr k → Expr k
  | .constant b => .constant (!b)
  | .atom a b => .atom a (!b)

structure Context (k n : ℕ) (states : Fin k → Fin 154) where
  config : Configuration n
  noCap : ¬config.HasCap 6
  noOctagon : ¬HasConvexNGon 8 (Finset.univ.image config.point)
  noJunction : Subsets.NoJunctionOn config.cup (Finset.range n)
  owner : Fin k → Fin n
  injective : Function.Injective owner
  owner_state : ∀ i, config.residualOwner noCap noOctagon noJunction (owner i) = states i
  nonzero : ∀ i j l, i ≠ j → i ≠ l → j ≠ l →
    orient (config.point (owner i)) (config.point (owner j)) (config.point (owner l)) ≠ 0

namespace Context
variable {k n : ℕ} {states : Fin k → Fin 154} (C : Context k n states)

def point (i : Fin k) : Point := C.config.point (C.owner i)

noncomputable def edge (i j : Fin k) : Label :=
  labels n C.config.cup (min (C.owner i).val (C.owner j).val)
    (max (C.owner i).val (C.owner j).val)

theorem edge_comm (i j : Fin k) : C.edge i j = C.edge j i := by
  simp only [edge, min_comm, max_comm]

theorem edge_of_lt {i j : Fin k} (h : C.owner i < C.owner j) :
    C.edge i j = labels n C.config.cup (C.owner i) (C.owner j) := by
  simp only [edge, min_eq_left (show (C.owner i).val ≤ (C.owner j).val from h.le),
    max_eq_right (show (C.owner i).val ≤ (C.owner j).val from h.le)]

theorem edge_bounds {i j : Fin k} (hij : i ≠ j) :
    1 ≤ (C.edge i j).1 ∧ (C.edge i j).1 ≤ 4 ∧
    1 ≤ (C.edge i j).2 ∧ (C.edge i j).2 ≤ 6 := by
  have ne := C.injective.ne hij
  rcases lt_or_gt_of_ne ne with h | h
  · rw [C.edge_of_lt h]
    exact label_bounds n C.config.cup
      (fun h => C.noCap (ListGeometry.hasCap_of_list C.config h))
      (C.config.residual_avoids_cup C.noOctagon) _ _ h (C.owner j).isLt
  · rw [C.edge_comm, C.edge_of_lt h]
    exact label_bounds n C.config.cup
      (fun h => C.noCap (ListGeometry.hasCap_of_list C.config h))
      (C.config.residual_avoids_cup C.noOctagon) _ _ h (C.owner i).isLt

noncomputable def atom : Atom k → Prop
  | .falsum => False
  | .before i j => C.owner i < C.owner j
  | .capGe i j t => t ≤ (C.edge i j).1
  | .cupGe i j t => t ≤ (C.edge i j).2
  | .positive i j l => 0 < orient (C.point i) (C.point j) (C.point l)
  | .convex i j l m => ConvexPosition {C.point i, C.point j, C.point l, C.point m}

noncomputable def holds : Expr k → Prop
  | .constant b => b = true
  | .atom a true => C.atom a
  | .atom a false => ¬ C.atom a

theorem holds_neg (e : Expr k) : C.holds e.neg ↔ ¬ C.holds e := by
  cases e with
  | constant b => cases b <;> simp [Expr.neg, holds]
  | atom a b => cases b <;> simp [Expr.neg, holds]

end Context

def before (i j : Fin k) : Expr k :=
  if i < j then .atom (.before i j) true else .atom (.before j i) false

def ge (cup : Bool) (i j : Fin k) (t : ℕ) : Expr k :=
  if t ≤ 1 then .constant true else
  if (if cup then 6 else 4) < t then .constant false else
  .atom (if cup then .cupGe (min i j) (max i j) t else .capGe (min i j) (max i j) t) true

/-- Canonical triple order, with the sign reversed for odd permutations. -/
def positive (i j l : Fin k) : Expr k :=
  if i < j then
    if j < l then .atom (.positive i j l) true
    else if i < l then .atom (.positive i l j) false
    else .atom (.positive l i j) true
  else
    if i < l then .atom (.positive j i l) false
    else if j < l then .atom (.positive j l i) true
    else .atom (.positive l j i) false

namespace Context
variable {k n : ℕ} {states : Fin k → Fin 154} (C : Context k n states)

theorem holds_before (i j : Fin k) (hij : i ≠ j) :
    C.holds (before i j) ↔ C.owner i < C.owner j := by
  unfold before
  split_ifs with h
  · rfl
  · simp only [holds, atom, not_lt]
    have ne := C.injective.ne hij
    omega

theorem holds_ge (cup : Bool) (i j : Fin k) (hij : i ≠ j) (t : ℕ) :
    C.holds (ge cup i j t) ↔ t ≤ (if cup then (C.edge i j).2 else (C.edge i j).1) := by
  have bounds := C.edge_bounds hij
  have edge : C.edge (min i j) (max i j) = C.edge i j := by
    rcases le_total i j with h | h
    · simp only [min_eq_left h, max_eq_right h]
    · simp only [min_eq_right h, max_eq_left h, C.edge_comm j i]
  cases cup <;> simp only [ge, Bool.false_eq_true, ↓reduceIte]
  all_goals split_ifs <;> simp [holds, atom, edge] <;> omega

private theorem sign_reverse (x : ℝ) (h : x ≠ 0) : (¬ 0 < -x) ↔ 0 < x := by
  constructor
  · intro hx
    have hle : 0 ≤ x := by linarith [le_of_not_gt hx]
    exact lt_of_le_of_ne hle h.symm
  · intro hx
    linarith

theorem holds_positive (i j l : Fin k) (hij : i ≠ j) (hil : i ≠ l) (hjl : j ≠ l) :
    C.holds (positive i j l) ↔ 0 < orient (C.point i) (C.point j) (C.point l) := by
  have hn := C.nonzero i j l hij hil hjl
  change orient (C.point i) (C.point j) (C.point l) ≠ 0 at hn
  unfold positive
  split_ifs
  · rfl
  · simp only [holds, atom, orient_swap (C.point i) (C.point j) (C.point l)]
    exact sign_reverse _ hn
  · simp only [holds, atom, orient_cycle (C.point l) (C.point i) (C.point j)]
  · have eq : orient (C.point j) (C.point i) (C.point l) =
        - orient (C.point i) (C.point j) (C.point l) := by simp only [orient]; ring
    simpa only [holds, atom, eq] using sign_reverse _ hn
  · simp only [holds, atom, orient_cycle (C.point j) (C.point l) (C.point i),
      orient_cycle (C.point l) (C.point i) (C.point j)]
  · have eq : orient (C.point l) (C.point j) (C.point i) =
        - orient (C.point i) (C.point j) (C.point l) := by simp only [orient]; ring
    simpa only [holds, atom, eq] using sign_reverse _ hn

end Context

/-- The exact directed Ferrers difference, with the forbidden junction cell removed. -/
def Allowed (states : Fin k → Fin 154) (i j : Fin k) (z : Label) : Prop :=
  Domains.Contains (ResidualDomains.shape (states j)) z ∧
  ¬ Domains.Contains (ResidualDomains.shape (states i)) z ∧ z ≠ (1, 6)

instance (states : Fin k → Fin 154) (i j : Fin k) (z : Label) :
    Decidable (Allowed states i j z) := by unfold Allowed; infer_instance

def emptyCheck (states : Fin k → Fin 154) (i j : Fin k) : Bool :=
  ResidualDomains.grid.all (fun z => decide (¬Allowed states i j z))

def domainClause (i j : Fin k) (a b : ℕ) : List (Expr k) :=
  [(before i j).neg, (ge false i j a).neg, ge false i j (a+1),
    (ge true i j b).neg, ge true i j (b+1)]

def growthClause (cup : Bool) (i j l : Fin k) (t : ℕ) : List (Expr k) :=
  [(before i j).neg, (before j l).neg,
    if cup then (positive i j l).neg else positive i j l,
    (ge cup i j t).neg, ge cup j l (t+1)]

namespace Context
variable {k n : ℕ} {states : Fin k → Fin 154} (C : Context k n states)
noncomputable def clause (xs : List (Expr k)) : Prop := ∃ e ∈ xs, C.holds e

@[simp] theorem clause_cons (x : Expr k) (xs : List (Expr k)) :
    C.clause (x::xs) ↔ C.holds x ∨ C.clause xs := by simp [clause]
@[simp] theorem clause_nil : ¬C.clause [] := by simp [clause]

theorem edge_allowed {i j : Fin k} (h : C.owner i < C.owner j) :
    Allowed states i j (C.edge i j) := by
  have hd := BlockGeometry.pair_difference n C.config.cup
    (fun h => C.noCap (ListGeometry.hasCap_of_list C.config h))
    (C.config.residual_avoids_cup C.noOctagon)
    (noJunction_of_lists n C.config.cup C.noJunction) (C.owner i) (C.owner j) h
  change Domains.Contains (ResidualDomains.shape
      (C.config.residualOwner C.noCap C.noOctagon C.noJunction (C.owner j))) _ ∧
    ¬Domains.Contains (ResidualDomains.shape
      (C.config.residualOwner C.noCap C.noOctagon C.noJunction (C.owner i))) _ at hd
  rw [C.owner_state i, C.owner_state j] at hd
  rw [C.edge_of_lt h]
  exact ⟨hd.1, hd.2, forbidden_label n C.config.cup
    (fun h => C.noCap (ListGeometry.hasCap_of_list C.config h))
    (noJunction_of_lists n C.config.cup C.noJunction) _ _ h (C.owner j).isLt⟩

theorem empty_clause (i j : Fin k) (ne : i ≠ j)
    (checked : emptyCheck states i j = true) : C.clause [(before i j).neg] := by
  simp only [clause_cons, clause_nil, or_false, holds_neg, C.holds_before i j ne]
  intro h
  have hh := List.all_eq_true.mp checked (C.edge i j)
    (ResidualDomains.mem_grid _ (C.edge_bounds ne))
  exact (of_decide_eq_true hh) (C.edge_allowed h)

theorem domain_clause (i j : Fin k) (ne : i ≠ j) (a b : ℕ)
    (checked : ¬Allowed states i j (a,b)) : C.clause (domainClause i j a b) := by
  simp only [domainClause, clause_cons, clause_nil, or_false, holds_neg,
    C.holds_before i j ne, C.holds_ge false i j ne, C.holds_ge true i j ne,
    Bool.false_eq_true, ↓reduceIte]
  by_contra! h
  have he : C.edge i j = (a,b) := Prod.ext (by omega) (by omega)
  exact checked (he ▸ C.edge_allowed h.1)

theorem transitive_clause (i j l : Fin k) (hij : i ≠ j) (hjl : j ≠ l) (hil : i ≠ l) :
    C.clause [(before i j).neg, (before j l).neg, before i l] := by
  simp only [clause_cons, clause_nil, or_false, holds_neg, C.holds_before i j hij,
    C.holds_before j l hjl, C.holds_before i l hil]
  by_contra! h
  exact (not_lt_of_ge h.2.2) (lt_trans h.1 h.2.1)

theorem growth_clause (cup : Bool) (i j l : Fin k) (hij : i ≠ j) (hjl : j ≠ l)
    (hil : i ≠ l) (t : ℕ) : C.clause (growthClause cup i j l t) := by
  have inc := labels_increasing n C.config.cup
    (fun h => C.noCap (ListGeometry.hasCap_of_list C.config h))
  cases cup <;>
    simp only [growthClause, Bool.false_eq_true, ↓reduceIte, clause_cons,
      clause_nil, or_false, holds_neg, C.holds_before i j hij,
      C.holds_before j l hjl, C.holds_positive i j l hij hil hjl,
      C.holds_ge false i j hij, C.holds_ge false j l hjl,
      C.holds_ge true i j hij, C.holds_ge true j l hjl,
      Bool.false_eq_true, ↓reduceIte]
  · by_contra! h
    have color : C.config.cup (C.owner i) (C.owner j) (C.owner l) = false := by
      apply Bool.eq_false_iff.mpr
      intro hc
      have hp := (C.config.cup_true_iff (C.owner i) (C.owner j) (C.owner l)).mp hc
      exact (not_lt_of_ge h.2.2.1) hp
    have growth := (inc _ _ _ h.1 h.2.1 (C.owner l).isLt).1 color
    rw [← C.edge_of_lt h.1, ← C.edge_of_lt h.2.1] at growth
    omega
  · by_contra! h
    have color := (C.config.cup_true_iff (C.owner i) (C.owner j) (C.owner l)).mpr h.2.2.1
    have growth := (inc _ _ _ h.1 h.2.1 (C.owner l).isLt).2 color
    rw [← C.edge_of_lt h.1, ← C.edge_of_lt h.2.1] at growth
    omega

theorem fixed_positive (i j l : Fin k) (hij : i ≠ j) (hjl : j ≠ l) (hil : i ≠ l)
    (checked : CycleSigns.CheckTriple ResidualDomains.computedTable
      (states i) (states j) (states l) = true) : C.clause [positive i j l] := by
  simp only [clause_cons, clause_nil, or_false, C.holds_positive i j l hij hil hjl]
  apply C.config.residual_positive_of_checked_states C.noCap C.noOctagon C.noJunction
    (C.owner i) (C.owner j) (C.owner l) (C.injective.ne hij) (C.injective.ne hjl)
    (C.injective.ne hil)
  simpa only [C.owner_state] using checked

theorem fixed_negative (i j l : Fin k) (hij : i ≠ j) (hjl : j ≠ l) (hil : i ≠ l)
    (checked : CycleSigns.CheckTriple ResidualDomains.computedTable
      (states i) (states l) (states j) = true) : C.clause [(positive i j l).neg] := by
  have hp := C.fixed_positive i l j hil hjl.symm hij checked
  simp only [clause_cons, clause_nil, or_false, C.holds_positive i l j hil hij hjl.symm,
    orient_swap (C.point i) (C.point j) (C.point l)] at hp
  simp only [clause_cons, clause_nil, or_false, holds_neg, C.holds_positive i j l hij hil hjl]
  linarith

end Context

/-- A literal that asserts disagreement with the specified Boolean pattern. -/
def disagree (e : Expr k) (b : Bool) : Expr k := if b then e.neg else e

def packetClause (i j l m : Fin k) (x y z w : Bool) : List (Expr k) :=
  [(before i j).neg, (before j l).neg, (before l m).neg,
    disagree (positive i j l) x, disagree (positive i j m) y,
    disagree (positive i l m) z, disagree (positive j l m) w]

def convexClause (i j l m : Fin k) (x y z w : Bool) : List (Expr k) :=
  [disagree (positive i j l) x, disagree (positive i j m) y,
    disagree (positive i l m) z, disagree (positive j l m) w,
    .atom (.convex i j l m) (decide ([!w,z,!y,x].count true = 2))]

namespace Context
variable {k n : ℕ} {states : Fin k → Fin 154} (C : Context k n states)

theorem disagree_false (e : Expr k) (b : Bool) (h : ¬C.holds (disagree e b)) :
    @decide (C.holds e) (Classical.propDecidable _) = b := by
  classical
  cases b <;> simp_all [disagree, C.holds_neg]

theorem packet_clause (i j l m : Fin k) (hij : i ≠ j) (hil : i ≠ l) (him : i ≠ m)
    (hjl : j ≠ l) (hjm : j ≠ m) (hlm : l ≠ m) (x y z w : Bool)
    (invalid : ¬PacketValid x y z w) : C.clause (packetClause i j l m x y z w) := by
  classical
  by_contra h
  simp only [packetClause, clause_cons, clause_nil, or_false, not_or,
    C.holds_neg, not_not, C.holds_before i j hij, C.holds_before j l hjl,
    C.holds_before l m hlm] at h
  obtain ⟨hij', hjl', hlm', hx, hy, hz, hw⟩ := h
  have px := C.disagree_false _ x hx
  have py := C.disagree_false _ y hy
  have pz := C.disagree_false _ z hz
  have pw := C.disagree_false _ w hw
  simp only [C.holds_positive i j l hij hil hjl] at px
  simp only [C.holds_positive i j m hij him hjm] at py
  simp only [C.holds_positive i l m hil him hlm] at pz
  simp only [C.holds_positive j l m hjl hjm hlm] at pw
  have packet := packetValid_of_xordered (C.point i) (C.point j) (C.point l) (C.point m)
    (C.config.xOrder hij') (C.config.xOrder hjl') (C.config.xOrder hlm')
  rw [px, py, pz, pw] at packet
  exact invalid packet

theorem convex_clause (i j l m : Fin k) (hij : i ≠ j) (hil : i ≠ l) (him : i ≠ m)
    (hjl : j ≠ l) (hjm : j ≠ m) (hlm : l ≠ m) (x y z w : Bool) :
    C.clause (convexClause i j l m x y z w) := by
  classical
  by_contra h
  simp only [convexClause, clause_cons, clause_nil, or_false, not_or] at h
  obtain ⟨hx, hy, hz, hw, hc⟩ := h
  have px := C.disagree_false _ x hx
  have py := C.disagree_false _ y hy
  have pz := C.disagree_false _ z hz
  have pw := C.disagree_false _ w hw
  simp only [C.holds_positive i j l hij hil hjl] at px
  simp only [C.holds_positive i j m hij him hjm] at py
  simp only [C.holds_positive i l m hil him hlm] at pz
  simp only [C.holds_positive j l m hjl hjm hlm] at pw
  have convex := convexPosition_four_iff_sign_count (C.point i) (C.point j) (C.point l) (C.point m)
    (C.nonzero i j l hij hil hjl) (C.nonzero i j m hij him hjm)
    (C.nonzero i l m hil him hlm) (C.nonzero j l m hjl hjm hlm)
  rw [px, py, pz, pw] at convex
  apply hc
  by_cases hb : [!w,z,!y,x].count true = 2
  · simpa only [hb, decide_true, holds, atom] using convex.mpr hb
  · simpa only [hb, decide_false, holds, atom] using mt convex.mp hb

theorem no_octagon_clause (s : Finset (Fin k)) (hs : s.card = 8) (xs : List (Expr k))
    (covered : ∀ i ∈ s, ∀ j ∈ s, ∀ l ∈ s, ∀ m ∈ s,
      i < j → j < l → l < m → Expr.atom (.convex i j l m) false ∈ xs) :
    C.clause xs := by
  classical
  have inj : Function.Injective C.point := C.config.point_injective.comp C.injective
  have sub : s.image C.point ⊆ Finset.univ.image C.config.point := by
    intro p hp
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hp
    exact Finset.mem_image.mpr ⟨C.owner i, Finset.mem_univ _, rfl⟩
  obtain ⟨i, hi, j, hj, l, hl, m, hm, hij, hjl, hlm, hc⟩ :=
    exists_nonconvex_quadruple_of_no_octagon C.point inj s hs _ sub C.noOctagon
  exact ⟨_, covered i hi j hj l hl m hm hij hjl hlm, hc⟩

end Context

/-- A literal template can discard false constants and reorder or repeat literals. -/
def covers (template clause : List (Expr k)) : Bool :=
  template.all (fun e => decide (e = .constant false ∨ e ∈ clause))

def decodeLiteral (vars : List (Atom k)) : Sat.Literal → Expr k
  | .pos i => .atom (vars.getD i .falsum) true
  | .neg i => .atom (vars.getD i .falsum) false

def decodeClause (vars : List (Atom k)) (clause : Sat.Clause) : List (Expr k) :=
  clause.map (decodeLiteral vars)

namespace Context
variable {k n : ℕ} {states : Fin k → Fin 154} (C : Context k n states)

theorem covered_clause (template xs : List (Expr k)) (ht : C.clause template)
    (checked : covers template xs = true) : C.clause xs := by
  obtain ⟨e, he, hh⟩ := ht
  have hc := of_decide_eq_true (List.all_eq_true.mp checked e he)
  rcases hc with hc | hc
  · subst e
    exact Bool.false_ne_true hh |>.elim
  · exact ⟨e, hc, hh⟩

noncomputable def valuation (vars : List (Atom k)) : Sat.Valuation :=
  fun i => C.atom (vars.getD i .falsum)

theorem satisfies_of_clause (vars : List (Atom k)) (cl : Sat.Clause)
    (h : C.clause (decodeClause vars cl)) : (C.valuation vars).satisfies cl := by
  classical
  induction cl with
  | nil => exact False.elim (C.clause_nil h)
  | cons l ls ih =>
    simp only [decodeClause, List.map_cons, clause_cons] at h
    intro hn
    rcases h with h | h
    · cases l with
      | pos i => exact False.elim (hn h)
      | neg i => exact False.elim (h hn)
    · exact ih h

end Context
end ErdosSzekeres.Omission.Coupled
