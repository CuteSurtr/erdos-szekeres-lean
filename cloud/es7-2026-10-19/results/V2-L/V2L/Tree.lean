import MirrorEncoding.Cover

/-!
# Tree-shaped cube covers

A cube-and-conquer run gives a tree: the top cubes of a case, and for every split cube `c` the
cubes `s` that `march_cu` produced under `c` (its children are `c ++ s`). `CTree.check` checks
that every list of sibling cubes is a cover (`Mir.coverCheck`), which needs only small kernel
computations, and `CTree.covers_of_check` turns that into `Mir.Covers` of the flat leaf list
`CTree.leaves`.
-/

namespace V2L

open ETV Mir

/-- A cube tree: a leaf, or a node whose children are pairs (relative cube, subtree). -/
inductive CTree where
  | leaf : CTree
  | node : List (List Int × CTree) → CTree

mutual
/-- The leaf cubes: `[[]]` for a leaf; for a node, every child's leaves prefixed by the
child's cube, in order. -/
def CTree.leaves : CTree → List (List Int)
  | .leaf => [[]]
  | .node kids => CTree.kidsLeaves kids

/-- The leaves of a list of children. -/
def CTree.kidsLeaves : List (List Int × CTree) → List (List Int)
  | [] => []
  | (s, t) :: rest => t.leaves.map (s ++ ·) ++ CTree.kidsLeaves rest
end

mutual
/-- Every sibling list is accepted by `Mir.coverCheck`. -/
def CTree.check : CTree → Bool
  | .leaf => true
  | .node kids => coverCheck (kids.map Prod.fst) && CTree.kidsCheck kids

/-- Every child tree checks. -/
def CTree.kidsCheck : List (List Int × CTree) → Bool
  | [] => true
  | (_, t) :: rest => t.check && CTree.kidsCheck rest
end

mutual
/-- All sibling lists of the tree, in preorder: a node's cube list first, then those of its
children in order. -/
def CTree.sibLists : CTree → List (List (List Int))
  | .leaf => []
  | .node kids => kids.map Prod.fst :: CTree.kidsSibLists kids

/-- The sibling lists of a list of children. -/
def CTree.kidsSibLists : List (List Int × CTree) → List (List (List Int))
  | [] => []
  | (_, t) :: rest => t.sibLists ++ CTree.kidsSibLists rest
end

mutual
/-- `check` is the conjunction of `coverCheck` over `sibLists`, so it can be proved from one
kernel computation per sibling list. -/
theorem CTree.check_of_sibLists : ∀ {t : CTree},
    (∀ L ∈ t.sibLists, coverCheck L = true) → t.check = true
  | .leaf, _ => by rw [CTree.check]
  | .node kids, h => by
    rw [CTree.sibLists] at h
    rw [CTree.check, Bool.and_eq_true]
    exact ⟨h _ List.mem_cons_self,
      CTree.kidsCheck_of_sibLists fun L hL => h L (List.mem_cons_of_mem _ hL)⟩

theorem CTree.kidsCheck_of_sibLists : ∀ {kids : List (List Int × CTree)},
    (∀ L ∈ CTree.kidsSibLists kids, coverCheck L = true) → CTree.kidsCheck kids = true
  | [], _ => by rw [CTree.kidsCheck]
  | (_, t) :: rest, h => by
    rw [CTree.kidsSibLists] at h
    rw [CTree.kidsCheck, Bool.and_eq_true]
    exact ⟨CTree.check_of_sibLists fun L hL => h L (List.mem_append_left _ hL),
      CTree.kidsCheck_of_sibLists fun L hL => h L (List.mem_append_right _ hL)⟩
end

theorem cubeSat_append {ν : ℕ → Bool} {s l : List ℤ} (hs : CubeSat ν s) (hl : CubeSat ν l) :
    CubeSat ν (s ++ l) := by
  intro z hz
  rcases List.mem_append.1 hz with h | h
  · exact hs z h
  · exact hl z h

theorem mem_kidsLeaves {kids : List (List Int × CTree)} {s : List Int} {t : CTree}
    (hk : (s, t) ∈ kids) {l : List Int} (hl : l ∈ t.leaves) : s ++ l ∈ CTree.kidsLeaves kids := by
  induction kids with
  | nil => simp at hk
  | cons k rest ih =>
    obtain ⟨s', t'⟩ := k
    rw [CTree.kidsLeaves, List.mem_append]
    rcases List.mem_cons.1 hk with h | h
    · cases h
      exact Or.inl (List.mem_map.2 ⟨l, hl, rfl⟩)
    · exact Or.inr (ih h)

theorem kidsCheck_mem {kids : List (List Int × CTree)} (h : CTree.kidsCheck kids = true)
    {s : List Int} {t : CTree} (hk : (s, t) ∈ kids) : t.check = true := by
  induction kids with
  | nil => simp at hk
  | cons k rest ih =>
    obtain ⟨s', t'⟩ := k
    rw [CTree.kidsCheck, Bool.and_eq_true] at h
    rcases List.mem_cons.1 hk with e | e
    · cases e
      exact h.1
    · exact ih h.2 e

mutual
/-- **Soundness of the tree check**: the leaves of a checked tree cover every assignment. -/
theorem CTree.covers_of_check : ∀ {t : CTree}, t.check = true → Covers t.leaves
  | .leaf, _ => fun _ => ⟨[], by simp [CTree.leaves], fun _ hz => by simp at hz⟩
  | .node kids, h => by
    rw [CTree.check, Bool.and_eq_true] at h
    intro ν
    obtain ⟨s, hs, hsat⟩ := covers_of_coverCheck h.1 ν
    obtain ⟨⟨s', t⟩, hk, rfl⟩ := List.mem_map.1 hs
    obtain ⟨l, hl, hlsat⟩ := CTree.covers_of_kidsCheck h.2 hk ν
    exact ⟨s' ++ l, by rw [CTree.leaves]; exact mem_kidsLeaves hk hl, cubeSat_append hsat hlsat⟩

theorem CTree.covers_of_kidsCheck : ∀ {kids : List (List Int × CTree)},
    CTree.kidsCheck kids = true → ∀ {s : List Int} {t : CTree}, (s, t) ∈ kids → Covers t.leaves
  | [], _, _, _, hk => by simp at hk
  | (s', t') :: rest, h, s, t, hk => by
    rw [CTree.kidsCheck, Bool.and_eq_true] at h
    rcases List.mem_cons.1 hk with e | e
    · cases e
      exact CTree.covers_of_check h.1
    · exact CTree.covers_of_kidsCheck h.2 e
end

/-- **Composition with the tree**: a checked tree whose leaf CNFs are all UNSAT refutes `F`. -/
theorem not_dimacsSatisfiable_of_tree {F : List (List ℤ)} {t : CTree} (h : t.check = true)
    (hleaf : ∀ l ∈ t.leaves, ¬DimacsSatisfiable (cubeCnf F l)) : ¬DimacsSatisfiable F :=
  not_dimacsSatisfiable_of_cover (CTree.covers_of_check h) hleaf

end V2L
