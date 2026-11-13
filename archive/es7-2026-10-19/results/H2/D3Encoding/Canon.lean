import D3Encoding.Families

/-!
# `canon` picks the lexicographic minimum of the orbit

Under the hypothesis `GroupClosed t` (the six maps are closed under composition on the
points `0, …, 3 t`, decidable for each `t`), `canon t (canon t Y) = canon t Y` for every
increasing list `Y` of points. Hence `canon` of a set is a key of the conv table.
-/

namespace D3

/-! ### `lexLt` -/

theorem lexLt_irrefl : ∀ a : List Nat, ¬lexLt a a
  | [] => by simp [lexLt]
  | x :: xs => by simp [lexLt, lexLt_irrefl xs]

theorem lexLt_trans : ∀ a b c : List Nat, lexLt a b → lexLt b c → lexLt a c
  | [], _, _, h, _ => by simp [lexLt] at h
  | _ :: _, [], _, h, _ => by simp [lexLt] at h
  | _ :: _, _ :: _, [], _, h => by simp [lexLt] at h
  | x :: xs, y :: ys, z :: zs, h1, h2 => by
    simp only [lexLt, Bool.or_eq_true, decide_eq_true_eq, Bool.and_eq_true, beq_iff_eq] at *
    rcases h1 with h1 | ⟨rfl, h1⟩ <;> rcases h2 with h2 | ⟨rfl, h2⟩
    · exact Or.inl (by omega)
    · exact Or.inl h1
    · exact Or.inl h2
    · exact Or.inr ⟨rfl, lexLt_trans xs ys zs h1 h2⟩

theorem lexLt_total : ∀ a b : List Nat, a.length = b.length → lexLt a b ∨ a = b ∨ lexLt b a
  | [], [], _ => Or.inr (Or.inl rfl)
  | [], _ :: _, h => by simp at h
  | _ :: _, [], h => by simp at h
  | x :: xs, y :: ys, h => by
    simp only [lexLt, Bool.or_eq_true, decide_eq_true_eq, Bool.and_eq_true, beq_iff_eq,
      List.cons.injEq]
    rcases Nat.lt_trichotomy x y with hxy | rfl | hxy
    · exact Or.inl (Or.inl hxy)
    · rcases lexLt_total xs ys (by simpa using h) with h' | h' | h'
      · exact Or.inl (Or.inr ⟨rfl, h'⟩)
      · exact Or.inr (Or.inl ⟨rfl, h'⟩)
      · exact Or.inr (Or.inr (Or.inr ⟨rfl, h'⟩))
    · exact Or.inr (Or.inr (Or.inl hxy))

/-- `¬ b < a` and `¬ c < b` give `¬ c < a`, for lists of one length. -/
theorem not_lexLt_trans {a b c : List Nat} (hab : a.length = b.length)
    (h1 : ¬lexLt a b) (h2 : ¬lexLt b c) : ¬lexLt a c := by
  intro h
  rcases lexLt_total a b hab with h' | rfl | h'
  · exact h1 h'
  · exact h2 h
  · exact h2 (lexLt_trans _ _ _ h' h)

/-! ### The fold in `canon` -/

theorem foldl_min (T : ((Nat → Nat) × Int) → List Nat) (n : Nat)
    (hT : ∀ g, (T g).length = n) :
    ∀ (gs : List ((Nat → Nat) × Int)) (b : List Nat), b.length = n →
      let r := gs.foldl (fun best g => if lexLt (T g) best then T g else best) b
      (r = b ∨ ∃ g ∈ gs, r = T g) ∧ ¬lexLt b r ∧ (∀ g ∈ gs, ¬lexLt (T g) r) ∧ r.length = n
  | [], b, hb => ⟨Or.inl rfl, lexLt_irrefl b, by simp, hb⟩
  | g :: gs, b, hb => by
    simp only [List.foldl_cons]
    have hb' : (if lexLt (T g) b then T g else b).length = n := by split <;> simp [hT, hb]
    obtain ⟨h1, h2, h3, h4⟩ := foldl_min T n hT gs _ hb'
    refine ⟨?_, ?_, ?_, h4⟩
    · rcases h1 with h1 | ⟨g', hg', h1⟩
      · rw [h1]; split
        · exact Or.inr ⟨g, List.mem_cons_self .., rfl⟩
        · exact Or.inl rfl
      · exact Or.inr ⟨g', List.mem_cons_of_mem _ hg', h1⟩
    · refine not_lexLt_trans (by rw [hb, hb']) ?_ h2
      split
      · rename_i h; intro h'; exact lexLt_irrefl _ (lexLt_trans _ _ _ h h')
      · exact lexLt_irrefl _
    · intro g' hg'
      rcases List.mem_cons.1 hg' with rfl | hg'
      · refine not_lexLt_trans (by rw [hT, hb']) ?_ h2
        split
        · exact lexLt_irrefl _
        · assumption
      · exact h3 g' hg'

/-- The orbit of `Y`: its sorted images under the six maps. -/
def orbit (t : Nat) (Y : List Nat) : List (List Nat) := (group t).map fun g => sortL (Y.map g.1)

/-- The six maps are closed under composition and division on the points `0, …, 3 t`. -/
def GroupClosed (t : Nat) : Prop :=
  ∀ g ∈ group t, ∀ h ∈ group t,
    (∃ k ∈ group t, ∀ i, i < 3 * t + 1 → g.1 (h.1 i) = k.1 i) ∧
    (∃ k ∈ group t, ∀ i, i < 3 * t + 1 → k.1 (h.1 i) = g.1 i)

theorem rot_zero {t i : Nat} (hi : i < 3 * t + 1) : rot (3 * t) 0 i = i := by
  unfold rot; split <;> omega

theorem sortL_of_sorted {Y : List Nat} (hY : Y.Pairwise (· < ·)) : sortL Y = Y := by
  unfold sortL
  apply List.mergeSort_of_sorted
  exact hY.imp fun h => by simp; omega

theorem sortL_sorted (l : List Nat) : (sortL l).Pairwise (fun a b => decide (a ≤ b) = true) :=
  List.sorted_mergeSort (le := fun a b => decide (a ≤ b))
    (fun a b c h1 h2 => by simp at *; omega) (fun a b => by simp; omega) l

theorem sortL_perm (l : List Nat) : (sortL l).Perm l := List.mergeSort_perm l _

theorem sortL_eq_of_perm {l l' : List Nat} (h : l.Perm l') : sortL l = sortL l' := by
  apply List.Perm.eq_of_sorted (le := fun a b => decide (a ≤ b) = true)
  · intro a b _ _ h1 h2; simp at h1 h2; omega
  · exact sortL_sorted l
  · exact sortL_sorted l'
  · exact (sortL_perm l).trans (h.trans (sortL_perm l').symm)

theorem length_sortL (l : List Nat) : (sortL l).length = l.length := (sortL_perm l).length_eq

theorem mem_sortL {l : List Nat} {x : Nat} : x ∈ sortL l ↔ x ∈ l := (sortL_perm l).mem_iff

/-- `canon` is the minimum of the orbit, and lies in it. -/
theorem canon_spec {t : Nat} {Y : List Nat} (hY : Y.Pairwise (· < ·))
    (hYP : ∀ y ∈ Y, y < 3 * t + 1) :
    canon t Y ∈ orbit t Y ∧ ∀ Z ∈ orbit t Y, ¬lexLt Z (canon t Y) := by
  have hT : ∀ g : (Nat → Nat) × Int, (sortL (Y.map g.1)).length = Y.length := by
    intro g; simp [length_sortL]
  obtain ⟨h1, h2, h3, -⟩ := foldl_min (fun g => sortL (Y.map g.1)) Y.length hT
    ((group t).drop 1) Y rfl
  have hid : sortL (Y.map (rot (3 * t) 0)) = Y := by
    rw [(List.map_congr_left fun y hy => rot_zero (hYP y hy)).trans (List.map_id Y)]
    exact sortL_of_sorted hY
  have hg : group t = (rot (3 * t) 0, 1) :: (group t).drop 1 := rfl
  refine ⟨?_, ?_⟩
  · unfold canon orbit
    rcases h1 with h1 | ⟨g, hg', h1⟩
    · rw [h1, hg, List.map_cons]; simp only at hid; rw [hid]; exact List.mem_cons_self ..
    · rw [h1]; exact List.mem_map_of_mem (List.mem_of_mem_drop hg')
  · intro Z hZ
    unfold orbit at hZ
    rw [hg, List.map_cons, List.mem_cons] at hZ
    rcases hZ with rfl | hZ
    · simp only at hid ⊢; rw [hid]; exact h2
    · obtain ⟨g, hg', rfl⟩ := List.mem_map.1 hZ
      exact h3 g hg'

theorem orbit_length {t : Nat} {Y Z : List Nat} (hZ : Z ∈ orbit t Y) : Z.length = Y.length := by
  unfold orbit at hZ
  obtain ⟨g, -, rfl⟩ := List.mem_map.1 hZ
  simp [length_sortL]

/-- The orbit of an image is the orbit. -/
theorem mem_orbit_image {t : Nat} (hG : GroupClosed t) {Y : List Nat}
    (hYP : ∀ y ∈ Y, y < 3 * t + 1) {h : (Nat → Nat) × Int} (hh : h ∈ group t) (Z : List Nat) :
    Z ∈ orbit t (sortL (Y.map h.1)) ↔ Z ∈ orbit t Y := by
  unfold orbit
  simp only [List.mem_map]
  have key : ∀ g : (Nat → Nat) × Int, sortL ((sortL (Y.map h.1)).map g.1) =
      sortL (Y.map fun y => g.1 (h.1 y)) := by
    intro g
    apply sortL_eq_of_perm
    have := ((sortL_perm (Y.map h.1)).map g.1)
    rw [List.map_map] at this
    exact this
  constructor
  · rintro ⟨g, hg, rfl⟩
    obtain ⟨⟨k, hk, hk'⟩, -⟩ := hG g hg h hh
    refine ⟨k, hk, ?_⟩
    rw [key]
    congr 1
    exact List.map_congr_left fun y hy => (hk' y (hYP y hy)).symm
  · rintro ⟨k, hk, rfl⟩
    obtain ⟨-, ⟨g, hg, hg'⟩⟩ := hG k hk h hh
    refine ⟨g, hg, ?_⟩
    rw [key]
    congr 1
    exact List.map_congr_left fun y hy => hg' y (hYP y hy)

/-- Members of the orbit are images under some map of the group. -/
theorem image_of_mem_orbit {t : Nat} {Y Z : List Nat} (hZ : Z ∈ orbit t Y) :
    ∃ g ∈ group t, Z = sortL (Y.map g.1) := by
  unfold orbit at hZ
  obtain ⟨g, hg, rfl⟩ := List.mem_map.1 hZ
  exact ⟨g, hg, rfl⟩

theorem sorted_image {t : Nat} {Y : List Nat} (hY : Y.Pairwise (· < ·))
    (hYP : ∀ y ∈ Y, y < 3 * t) {g : (Nat → Nat) × Int} (hg : g ∈ group t) :
    (sortL (Y.map g.1)).Pairwise (· < ·) ∧ ∀ y ∈ sortL (Y.map g.1), y < 3 * t := by
  obtain ⟨hlt, hlt', hinj, -⟩ := group_perm g hg
  have hnd : (Y.map g.1).Nodup := by
    show (Y.map g.1).Pairwise (· ≠ ·)
    rw [List.pairwise_map]
    exact hY.imp_of_mem fun hx hy hxy h => Nat.ne_of_lt hxy
      (hinj _ _ (by have := hYP _ hx; omega) (by have := hYP _ hy; omega) h)
  have hnd' : (sortL (Y.map g.1)).Nodup := (sortL_perm _).nodup_iff.2 hnd
  refine ⟨?_, ?_⟩
  · have h1 := sortL_sorted (Y.map g.1)
    have h2 : (sortL (Y.map g.1)).Pairwise (· ≠ ·) := hnd'
    exact (h1.and h2).imp fun ⟨a, b⟩ => by simp at a; omega
  · intro y hy
    rw [mem_sortL, List.mem_map] at hy
    obtain ⟨x, hx, rfl⟩ := hy
    exact hlt' x (hYP x hx)

/-- `canon` is idempotent, so `canon` of a set of points is a canonical key. -/
theorem canon_canon {t : Nat} (hG : GroupClosed t) {Y : List Nat} (hY : Y.Pairwise (· < ·))
    (hYP : ∀ y ∈ Y, y < 3 * t) : canon t (canon t Y) = canon t Y := by
  have hYP' : ∀ y ∈ Y, y < 3 * t + 1 := fun y hy => by have := hYP y hy; omega
  obtain ⟨hm, hmin⟩ := canon_spec hY hYP'
  obtain ⟨h, hh, hZ⟩ := image_of_mem_orbit hm
  obtain ⟨hZs, hZP⟩ := sorted_image hY hYP hh
  rw [← hZ] at hZs hZP
  have hZP' : ∀ y ∈ canon t Y, y < 3 * t + 1 := fun y hy => by have := hZP y hy; omega
  obtain ⟨hm2, hmin2⟩ := canon_spec hZs hZP'
  have e : ∀ W, W ∈ orbit t (canon t Y) ↔ W ∈ orbit t Y := by
    intro W; rw [hZ]; exact mem_orbit_image hG hYP' hh W
  have l1 := orbit_length hm2
  have l2 := orbit_length hm
  rcases lexLt_total (canon t (canon t Y)) (canon t Y) (by rw [l1]) with h1 | h1 | h1
  · exact absurd h1 (hmin _ ((e _).1 hm2))
  · exact h1
  · exact absurd h1 (hmin2 _ ((e _).2 hm))

end D3
