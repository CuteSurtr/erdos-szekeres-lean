import V2L.Data
import V2L.Tree

/-!
# Helpers for the generated cube-tree data (`V2L/Trees/`)

A cube is stored as `(k, n)` with 5 hex digits per literal (leaf cubes branch on auxiliary
variables up to 47002), in the literal encoding of `V2L.Data` (`decLit`).
-/

namespace V2L

/-- Read the low `k` base-2^20 digits of `n`, most significant first. -/
def unpackT : Nat → Nat → List Int → List Int
  | 0, _, acc => acc
  | k + 1, n, acc => unpackT k (n / 1048576) (decLit (n % 1048576) :: acc)

/-- A child that is a leaf. -/
def lf (k n : Nat) : List Int × CTree := (unpackT k n [], .leaf)

/-- A child that is split further. -/
def nd (k n : Nat) (kids : List (List Int × CTree)) : List Int × CTree :=
  (unpackT k n [], .node kids)

/-- `P` holds at every element, as a list of proofs (to combine per-case theorems). -/
inductive AllOf {α : Type} (P : α → Prop) : List α → Prop
  | nil : AllOf P []
  | cons {a : α} {l : List α} : P a → AllOf P l → AllOf P (a :: l)

theorem AllOf.forall {α : Type} {P : α → Prop} {l : List α} (h : AllOf P l) : ∀ a ∈ l, P a := by
  induction h with
  | nil => intro a ha; simp at ha
  | cons hp _ ih =>
    intro a ha
    rcases List.mem_cons.1 ha with rfl | ha
    · exact hp
    · exact ih a ha

end V2L
