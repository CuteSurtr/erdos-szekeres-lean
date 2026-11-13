/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, ES8PlanarChains.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: real points as Fin 2 → ℝ, local geometry and namespaces, Lean 4.24.
-/
import ErdosSzekeres.Omission.Realization

/-! Geometric chain closure. Consecutive triple colours alone do not justify
subsequence closure in an arbitrary Config; the real-plane four-point identities
supply the missing hypothesis here. -/
namespace ErdosSzekeres.Omission.PlanarChains
open ErdosSzekeres

theorem four_point_identity_left (a b c d : Point) :
    (c 0-b 0)*orient a b d = (d 0-b 0)*orient a b c + (b 0-a 0)*orient b c d := by
  unfold orient; ring

theorem four_point_identity_right (a b c d : Point) :
    (c 0-b 0)*orient a c d = (d 0-c 0)*orient a b c + (c 0-a 0)*orient b c d := by
  unfold orient; ring

theorem positive_four (a b c d : Point) (ab : a 0<b 0) (bc : b 0<c 0)
    (cd : c 0<d 0) (abc : 0<orient a b c) (bcd : 0<orient b c d) :
    0<orient a b d ∧ 0<orient a c d := by
  have h1 := four_point_identity_left a b c d
  have h2 := four_point_identity_right a b c d
  have p1 := mul_pos (show 0<d 0-b 0 by linarith) abc
  have p2 := mul_pos (show 0<b 0-a 0 by linarith) bcd
  have p3 := mul_pos (show 0<d 0-c 0 by linarith) abc
  have p4 := mul_pos (show 0<c 0-a 0 by linarith) bcd
  exact ⟨(mul_pos_iff_of_pos_left (sub_pos.mpr bc)).mp (by linarith),
    (mul_pos_iff_of_pos_left (sub_pos.mpr bc)).mp (by linarith)⟩

theorem negative_four (a b c d : Point) (ab : a 0<b 0) (bc : b 0<c 0)
    (cd : c 0<d 0) (abc : orient a b c<0) (bcd : orient b c d<0) :
    orient a b d<0 ∧ orient a c d<0 := by
  have h1 := four_point_identity_left a b c d
  have h2 := four_point_identity_right a b c d
  have p1 := mul_neg_of_pos_of_neg (show 0<d 0-b 0 by linarith) abc
  have p2 := mul_neg_of_pos_of_neg (show 0<b 0-a 0 by linarith) bcd
  have p3 := mul_neg_of_pos_of_neg (show 0<d 0-c 0 by linarith) abc
  have p4 := mul_neg_of_pos_of_neg (show 0<c 0-a 0 by linarith) bcd
  constructor
  · by_contra h
    have := mul_nonneg (le_of_lt (sub_pos.mpr bc)) (le_of_not_gt h)
    linarith
  · by_contra h
    have := mul_nonneg (le_of_lt (sub_pos.mpr bc)) (le_of_not_gt h)
    linarith

variable {α : Type*} [LinearOrder α]

def OrderedTriples (R : α→α→α→Prop) (l : List α) : Prop :=
  ∀ a∈l, ∀ b∈l, ∀ c∈l, a<b → b<c → R a b c

/-- Transitivity is required only on the ambient domain containing this chain. -/
theorem chain3_all (R : α→α→α→Prop) (S : Set α)
    (trans : ∀ a∈S, ∀ b∈S, ∀ c∈S, ∀ d∈S,
      a<b → b<c → c<d → R a b c → R b c d → R a b d ∧ R a c d)
    (l : List α) (inside : ∀ a∈l, a∈S) (sorted : l.Pairwise (·<·))
    (chain : l.Chain3' R) : OrderedTriples R l := by
  induction l with
  | nil => simp [OrderedTriples]
  | cons a l ih =>
    have ord := List.pairwise_cons.mp sorted
    have tail := ih (fun x hx => inside x (by simp [hx])) ord.2 chain.tail
    intro x hx y hy z hz xy yz
    rcases List.mem_cons.mp hx with rfl | hx
    · have hy' : y∈l := (List.mem_cons.mp hy).resolve_left (ne_of_gt xy)
      have hz' : z∈l := (List.mem_cons.mp hz).resolve_left (ne_of_gt (lt_trans xy yz))
      cases l with
      | nil => simp at hy'
      | cons b l =>
        have heads : ∀ c∈l, R x b c := by
          cases l with
          | nil => simp
          | cons c rest =>
            have abc := (List.chain3'_cons.mp chain).1
            intro d hd
            rcases List.mem_cons.mp hd with rfl | hd
            · exact abc
            · have bc := (List.pairwise_cons.mp ord.2).1 c (by simp)
              have cd := (List.pairwise_cons.mp (List.pairwise_cons.mp ord.2).2).1 d hd
              have bcd := tail b (by simp) c (by simp) d (by simp [hd]) bc cd
              exact (trans x (inside x (by simp)) b (inside b (by simp))
                c (inside c (by simp)) d (inside d (by simp [hd]))
                (ord.1 b (by simp)) bc cd abc bcd).1
        rcases List.mem_cons.mp hy' with rfl | hy'
        · exact heads z ((List.mem_cons.mp hz').resolve_left (ne_of_gt yz))
        · have bz := (List.mem_cons.mp hz').resolve_left (ne_of_gt
            (lt_trans ((List.pairwise_cons.mp ord.2).1 y hy') yz))
          have by' := (List.pairwise_cons.mp ord.2).1 y hy'
          exact (trans x (inside x (by simp)) b (inside b (by simp))
            y (inside y (by simp [hy'])) z (inside z (by simp [bz]))
            (ord.1 b (by simp)) by' yz (heads y hy')
            (tail b (by simp) y (by simp [hy']) z (by simp [bz]) by' yz)).2
    · have hy' : y∈l := (List.mem_cons.mp hy).resolve_left (by
        intro he; subst y; exact (lt_asymm xy (ord.1 x hx)))
      have hz' : z∈l := (List.mem_cons.mp hz).resolve_left (by
        intro he; subst z; exact (lt_asymm (lt_trans xy yz) (ord.1 x hx)))
      exact tail x hx y hy' z hz' xy yz

/-- Actual planar cup chains have every ordered triple positive. -/
theorem cup_all {n} (c : Configuration n) (l : List (Fin n))
    (sorted : l.IsChain (·<·))
    (chain : l.Chain3' (fun u v w => 0<orient (c.point u) (c.point v) (c.point w))) :
    OrderedTriples (fun u v w => 0<orient (c.point u) (c.point v) (c.point w)) l := by
  apply chain3_all _ Set.univ _ l (by simp) sorted.pairwise chain
  intro a _ b _ d _ e _ ab bd de h1 h2
  exact positive_four _ _ _ _ (c.xOrder ab) (c.xOrder bd) (c.xOrder de) h1 h2

end ErdosSzekeres.Omission.PlanarChains
