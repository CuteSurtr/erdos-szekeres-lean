import ErdosSzekeres.Omission.ResidualCycleGeometry
import ErdosSzekeres.Omission.CoupledSemantics
import ErdosSzekeres.OrientationPackets
import RowEnc.Enc

/-!
# RowGeo.Geo: the geometric facts the encoder needs beyond `Coupled` (Mathlib side)

* `stateTable_eq`, `st_eq_shape`, `grid46_eq`: the Std-only state table and grid are the library's
  `ResidualCatalog.catalog` and `ResidualDomains.grid` (kernel check of the literal data).
* `allowedB_iff`, `emptyB_spec`: the difference tests are the library's `Coupled.Allowed`/`emptyCheck` (F3, F4).
* `bbox_valid`: the bounding box of the plain difference passes `ResidualDomains.valid` (every label of the
  difference fits), for any two states; `checkTriple_of_ttB`, `positive_of_ttB`: the six-order test forces the
  orientation of actual owners (F7), as `residual_positive_of_checked_states` does for `computedTable`.
* `cup_label_le_h1`: the source-cup bound (F2): for actual owners `a < b`, the cup label of `(a, b)` is at most
  `h₁(state a) + 1` (drop `b` from a longest cup ending with `(a, b)`; its last edge `(t, a)` gives the incoming
  label `(1, d₂(t, a))` of `a`).
* `bad4_invalid`: the BAD4 patterns are exactly not `PacketValid` (F8).
-/

namespace RowGeo
open RowEnc ErdosSzekeres ErdosSzekeres.Omission

set_option maxRecDepth 20000 in
theorem stateTable_eq : stateTable = ResidualCatalog.catalog := by decide +kernel

theorem st_eq_shape (s : ℕ) : st s = ResidualDomains.shape s := by
  unfold st ResidualDomains.shape
  rw [stateTable_eq]

theorem grid46_eq : grid46 = ResidualDomains.grid := rfl

theorem cont_iff (sh : List ℕ) (z : ℕ × ℕ) : cont sh z.1 z.2 = true ↔ Domains.Contains sh z := by
  simp [cont, Domains.Contains]

theorem allowedB_iff {k : ℕ} (states : Fin k → Fin 154) (i j : Fin k) (z : ℕ × ℕ) :
    allowedB (states i) (states j) z = true ↔ Coupled.Allowed states i j z := by
  unfold allowedB Coupled.Allowed
  rw [st_eq_shape, st_eq_shape]
  simp only [Bool.and_eq_true, Bool.not_eq_true', cont_iff]
  constructor
  · rintro ⟨⟨h1, h2⟩, h3⟩
    refine ⟨h1, fun h => ?_, fun h => ?_⟩
    · have := (cont_iff _ z).2 h; simp_all
    · subst h; simp at h3
  · rintro ⟨h1, h2, h3⟩
    refine ⟨⟨h1, ?_⟩, ?_⟩
    · cases hc : cont (ResidualDomains.shape ↑(states i)) z.1 z.2
      · rfl
      · exact absurd ((cont_iff _ z).1 hc) h2
    · obtain ⟨a, b⟩ := z
      simp only [Bool.and_eq_false_imp, beq_iff_eq]
      intro ha; subst ha
      exact beq_eq_false_iff_ne.2 fun hb => h3 (by rw [hb])

theorem emptyB_spec {k : ℕ} (states : Fin k → Fin 154) (i j : Fin k) (h : emptyB (states i) (states j) = true) :
    Coupled.emptyCheck states i j = true := by
  unfold emptyB at h
  unfold Coupled.emptyCheck
  rw [← grid46_eq]
  refine List.all_eq_true.2 fun z hz => ?_
  have := List.all_eq_true.1 h z hz
  simp only [Bool.not_eq_true'] at this
  exact decide_eq_true fun ha => by rw [(allowedB_iff states i j z).2 ha] at this; exact absurd this (by simp)

/-! ## Bounding boxes -/

def toBox (b : BoxS) : Domains.Box := ⟨b.present, b.xmin, b.xmax, b.ymin, b.ymax⟩

theorem foldl_min_le (f : ℕ × ℕ → ℕ) : ∀ (l : List (ℕ × ℕ)) (a : ℕ),
    l.foldl (fun m w => min m (f w)) a ≤ a ∧ ∀ x ∈ l, l.foldl (fun m w => min m (f w)) a ≤ f x
  | [], a => ⟨le_refl a, fun _ hx => absurd hx List.not_mem_nil⟩
  | b :: l, a => by
    obtain ⟨h1, h2⟩ := foldl_min_le f l (min a (f b))
    simp only [List.foldl_cons]
    refine ⟨le_trans h1 (min_le_left _ _), fun x hx => ?_⟩
    rcases List.mem_cons.1 hx with rfl | hx
    · exact le_trans h1 (min_le_right _ _)
    · exact h2 x hx

theorem le_foldl_max (f : ℕ × ℕ → ℕ) : ∀ (l : List (ℕ × ℕ)) (a : ℕ),
    a ≤ l.foldl (fun m w => max m (f w)) a ∧ ∀ x ∈ l, f x ≤ l.foldl (fun m w => max m (f w)) a
  | [], a => ⟨le_refl a, fun _ hx => absurd hx List.not_mem_nil⟩
  | b :: l, a => by
    obtain ⟨h1, h2⟩ := le_foldl_max f l (max a (f b))
    simp only [List.foldl_cons]
    refine ⟨le_trans (le_max_left _ _) h1, fun x hx => ?_⟩
    rcases List.mem_cons.1 hx with rfl | hx
    · exact le_trans (le_max_right _ _) h1
    · exact h2 x hx

theorem fits_bbox (sa sb : ℕ) (z : ℕ × ℕ) (hz : z ∈ diffCells sa sb) : Domains.Fits (toBox (bbox sa sb)) z := by
  unfold bbox
  generalize hd : diffCells sa sb = d at hz
  cases d with
  | nil => exact absurd hz List.not_mem_nil
  | cons w ws =>
    simp only [toBox, Domains.Fits]
    have a1 := foldl_min_le Prod.fst ws w.1
    have a2 := le_foldl_max Prod.fst ws w.1
    have a3 := foldl_min_le Prod.snd ws w.2
    have a4 := le_foldl_max Prod.snd ws w.2
    rcases List.mem_cons.1 hz with rfl | hz
    · exact ⟨trivial, a1.1, a2.1, a3.1, a4.1⟩
    · exact ⟨trivial, a1.2 z hz, a2.2 z hz, a3.2 z hz, a4.2 z hz⟩

/-- **The Std box is valid** for every pair of states. -/
theorem bbox_valid (sa sb : ℕ) :
    ResidualDomains.valid (ResidualDomains.shape sa) (ResidualDomains.shape sb) (toBox (bbox sa sb)) = true := by
  unfold ResidualDomains.valid
  refine List.all_eq_true.2 fun z hz => decide_eq_true fun hd => fits_bbox sa sb z ?_
  unfold diffCells
  refine List.mem_filter.2 ⟨by rw [grid46_eq]; exact hz, ?_⟩
  rw [st_eq_shape, st_eq_shape]
  simp only [Bool.and_eq_true, Bool.not_eq_true']
  refine ⟨(cont_iff _ z).2 hd.1, ?_⟩
  cases hc : cont (ResidualDomains.shape sa) z.1 z.2
  · rfl
  · exact absurd ((cont_iff _ z).1 hc) hd.2

theorem safeB_iff (ab bc ac : BoxS) (want : Bool) :
    safeB ab bc ac want = true ↔ CycleSigns.Safe (toBox ab) (toBox bc) (toBox ac) want := by
  unfold safeB CycleSigns.Safe toBox
  cases want <;> simp [Bool.or_eq_true, or_assoc]

theorem checkTriple_of_ttB (a b c : ℕ) (h : ttB a b c = true) :
    CycleSigns.CheckTriple (fun x y => toBox (bbox x y)) a b c = true := by
  unfold ttB at h
  simp only [Bool.and_eq_true, safeB_iff] at h
  unfold CycleSigns.CheckTriple
  obtain ⟨⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩, h6⟩ := h
  exact decide_eq_true ⟨h1, h2, h3, h4, h5, h6⟩

/-- **F7**: the six-order test on the owners' states forces a positive orientation (the proof of
`Configuration.residual_positive_of_checked_states` with the Std table). -/
theorem positive_of_ttB {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (u v w : Fin n) (huv : u ≠ v) (hvw : v ≠ w) (huw : u ≠ w)
    (checked : ttB (c.residualOwner noCap noOctagon noJunction u) (c.residualOwner noCap noOctagon noJunction v)
      (c.residualOwner noCap noOctagon noJunction w) = true) :
    0 < orient (c.point u) (c.point v) (c.point w) := by
  apply CycleSigns.checked_triple_positive n (fun x y => toBox (bbox x y))
    (fun i => (c.residualOwner noCap noOctagon noJunction i).val) c.cup (ResidualRanks.labels n c.cup) c.point
    (ResidualRanks.labels_increasing n c.cup (fun h => noCap (ListGeometry.hasCap_of_list c h))) ?_ ?_
    c.generalPosition u v w huv hvw huw (checkTriple_of_ttB _ _ _ checked)
  · intro a b hab
    exact ResidualDomains.actual_pair_fits n c.cup (fun h => noCap (ListGeometry.hasCap_of_list c h))
      (c.residual_avoids_cup noOctagon) (ResidualRanks.noJunction_of_lists n c.cup noJunction)
      a b hab _ (bbox_valid _ _)
  · intro a b d _ _
    exact c.cup_true_iff a b d

/-! ## F2: the source-cup bound -/

theorem ending_cases {cup : ℕ → ℕ → ℕ → Bool} {u v len : ℕ} (p : ActualRanks.EndingPath cup true u v len) :
    len = 2 ∨ ∃ t l, len = l + 1 ∧ ActualRanks.EndingPath cup true t u l := by
  cases p with
  | pair _ => exact Or.inl rfl
  | step p _ _ => exact Or.inr ⟨_, _, rfl, p⟩

theorem cup_label_le_h1 {n : ℕ} (c : Configuration n) (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (a b : Fin n) (hab : a < b) :
    (ResidualRanks.labels n c.cup a b).2 ≤
      (ResidualDomains.shape (c.residualOwner noCap noOctagon noJunction a)).getD 0 0 + 1 := by
  have caps : ¬(ActualRanks.colorConfig c.cup true).HasNCap 6 (Finset.range n) :=
    fun h => noCap (ListGeometry.hasCap_of_list c h)
  have cups := c.residual_avoids_cup noOctagon
  have junction := ResidualRanks.noJunction_of_lists n c.cup noJunction
  have path := ActualRanks.rank_attained c.cup true a b hab
  rcases ending_cases path with h2 | ⟨t, l, hl, p⟩
  · simp only [ResidualRanks.labels, h2]; omega
  · have hta := (ActualRanks.length_bounds p).2.2
    have hge := ActualRanks.rank_ge p
    have bd := ResidualRanks.label_bounds n c.cup caps cups t a hta a.isLt
    have hin : StateInterface.Incoming (ResidualRanks.labels n c.cup) a
        (1, (ResidualRanks.labels n c.cup t a).2) := ⟨t, hta, bd.1, le_refl _⟩
    have hcont := (ResidualDomains.owner_contains n c.cup caps cups junction a
      (1, (ResidualRanks.labels n c.cup t a).2) ⟨le_refl _, by omega, bd.2.2.1, bd.2.2.2⟩).2 hin
    have hown : c.residualOwner noCap noOctagon noJunction a =
        ResidualCatalog.ownerIndex n c.cup caps cups junction a := rfl
    rw [hown]
    simp only [Domains.Contains, Nat.sub_self] at hcont
    simp only [ResidualRanks.labels] at hcont ⊢
    omega

/-! ## F8 -/

theorem bad4_invalid : ∀ x ∈ bad4, ¬ PacketValid x.1 x.2.1 x.2.2.1 x.2.2.2 := by decide

end RowGeo
