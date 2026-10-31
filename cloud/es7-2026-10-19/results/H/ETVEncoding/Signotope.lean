import ErdosSzekeres.OrientationPackets

/-!
# Signotopes, caps, cups and gons

Points are the natural numbers `0, …, N-1` in increasing x-order. A signotope assigns a sign
to every increasing triple; `σ i j k = true` means counterclockwise, i.e. `j` lies below the
segment `ik` (a *cup triple*), and `false` means a *cap triple*. This is the convention of
`gen_cnf.py` / `gen_etv.py`.

The 4-point axiom is the repository's `PacketValid` (the four signs of `ijk, ijl, ikl, jkl`
change at most once); the eight CNF clauses of a quadruple express exactly this.

A *chain of type `t`* is a strictly increasing list of points whose consecutive triples all
have sign `t`: a cap for `t = false`, a cup for `t = true`. A `K`-gon is a cap and a cup with
common first and last point and `K + 2` points in total (counted with the two shared ends),
as in Baek's `Config.NGon`.
-/

namespace ETV

open ErdosSzekeres (PacketValid)

/-- Orientation data on the points `0, 1, 2, …`; only increasing triples are used. -/
abbrev Sig := ℕ → ℕ → ℕ → Bool

/-- `σ` is a signotope on the points `0, …, N-1`. -/
def IsSignotope (N : ℕ) (σ : Sig) : Prop :=
  ∀ i j k l, i < j → j < k → k < l → l < N →
    PacketValid (σ i j k) (σ i j l) (σ i k l) (σ j k l)

/-! ### Elementary consequences of the 4-point axiom -/

section Packet

variable {a b c d : Bool}

theorem pv_outer (h : PacketValid a b c d) (had : a = d) : b = a ∧ c = a := by
  revert h had; cases a <;> cases b <;> cases c <;> cases d <;> decide

theorem pv_ne13 (h : PacketValid a b c d) (hac : a ≠ c) : d = c := by
  revert h hac; cases a <;> cases b <;> cases c <;> cases d <;> decide

theorem pv_ne24 (h : PacketValid a b c d) (hbd : b ≠ d) : a = b := by
  revert h hbd; cases a <;> cases b <;> cases c <;> cases d <;> decide

theorem pv_ne23 (h : PacketValid a b c d) (hbc : b ≠ c) : a = b ∧ d = c := by
  revert h hbc; cases a <;> cases b <;> cases c <;> cases d <;> decide

/-- The eight clauses of a quadruple: no pattern `+-+` or `-+-` on three of the four
positions. -/
theorem pv_no_alt (h : PacketValid a b c d) :
    ¬(a = c ∧ a ≠ b) ∧ ¬(a = d ∧ a ≠ b) ∧ ¬(a = d ∧ a ≠ c) ∧ ¬(b = d ∧ b ≠ c) := by
  revert h; cases a <;> cases b <;> cases c <;> cases d <;> decide

end Packet

/-! ### Chains (caps and cups) -/

/-- `Chain σ t l`: `l` is strictly increasing and every three consecutive points of `l` form a
triple of sign `t` (a cap for `t = false`, a cup for `t = true`). -/
def Chain (σ : Sig) (t : Bool) : List ℕ → Prop
  | a :: b :: c :: l => a < b ∧ σ a b c = t ∧ Chain σ t (b :: c :: l)
  | [a, b] => a < b
  | _ => True

/-- There is an `m`-point chain of sign `t` among the points `0, …, N-1`. -/
def HasChain (σ : Sig) (N : ℕ) (t : Bool) (m : ℕ) : Prop :=
  ∃ l : List ℕ, l.length = m ∧ (∀ p ∈ l, p < N) ∧ Chain σ t l

/-- `HasCap σ N a`: an `a`-cap. -/
abbrev HasCap (σ : Sig) (N a : ℕ) : Prop := HasChain σ N false a

/-- `HasCup σ N u`: a `u`-cup. -/
abbrev HasCup (σ : Sig) (N u : ℕ) : Prop := HasChain σ N true u

/-- A `K`-gon: a cap `l₁` and a cup `l₂` with the same first and the same last point and
`|l₁| + |l₂| = K + 2`. -/
def HasGon (σ : Sig) (N K : ℕ) : Prop :=
  ∃ l₁ l₂ : List ℕ, Chain σ false l₁ ∧ Chain σ true l₂ ∧ 2 ≤ l₁.length ∧ 2 ≤ l₂.length ∧
    l₁.head? = l₂.head? ∧ l₁.getLast? = l₂.getLast? ∧ l₁.length + l₂.length = K + 2 ∧
    (∀ p ∈ l₁, p < N) ∧ (∀ p ∈ l₂, p < N)

variable {σ : Sig} {t : Bool} {N : ℕ}

theorem chain_cons {a : ℕ} {l : List ℕ} :
    Chain σ t (a :: l) ↔ (∀ b, l.head? = some b → a < b) ∧
      (∀ b c, l.take 2 = [b, c] → σ a b c = t) ∧ Chain σ t l := by
  match l with
  | [] => simp [Chain]
  | [b] => simp [Chain]
  | b :: c :: m => simp [Chain]

theorem Chain.tail {a : ℕ} {l : List ℕ} (h : Chain σ t (a :: l)) : Chain σ t l :=
  (chain_cons.1 h).2.2

theorem Chain.head_lt : ∀ {a : ℕ} {l : List ℕ}, Chain σ t (a :: l) → ∀ q ∈ l, a < q
  | _, [], _, q, hq => by simp at hq
  | _, [b], h, q, hq => by
      simp only [List.mem_singleton] at hq
      subst hq
      exact h
  | _, b :: c :: l, h, q, hq => by
      rcases List.mem_cons.1 hq with rfl | hq
      · exact h.1
      · exact lt_trans h.1 (Chain.head_lt h.2.2 q hq)

theorem Chain.pairwise : ∀ {l : List ℕ}, Chain σ t l → l.Pairwise (· < ·)
  | [], _ => List.Pairwise.nil
  | _ :: _, h => List.Pairwise.cons (Chain.head_lt h) (Chain.pairwise h.tail)

/-- Appending a point to a chain. -/
theorem Chain.snoc : ∀ (l : List ℕ) {w a b : ℕ}, Chain σ t (l ++ [w, a]) → a < b →
    σ w a b = t → Chain σ t (l ++ [w, a] ++ [b])
  | [], w, a, b, h, hab, hwab => by
      simp only [List.nil_append, List.cons_append, Chain] at h ⊢
      exact ⟨h, hwab, hab⟩
  | p :: l, w, a, b, h, hab, hwab => by
      have hlen : 2 ≤ (l ++ [w, a]).length := by simp
      have hne : l ++ [w, a] ≠ [] := by simp
      rw [List.cons_append, List.cons_append] at *
      rw [chain_cons] at h ⊢
      obtain ⟨h1, h2, h3⟩ := h
      refine ⟨?_, ?_, Chain.snoc l h3 hab hwab⟩
      · intro q hq
        apply h1 q
        rw [List.head?_append] at hq
        cases hl : (l ++ [w, a]).head? with
        | none => simp_all
        | some z => simp_all
      · intro q r hqr
        apply h2 q r
        rwa [List.take_append_of_le_length hlen] at hqr

/-- Every three points of a chain, not only consecutive ones, form a triple of sign `t`. -/
def AllTriples (σ : Sig) (t : Bool) (l : List ℕ) : Prop :=
  ∀ p ∈ l, ∀ q ∈ l, ∀ r ∈ l, p < q → q < r → σ p q r = t

theorem Chain.allTriples (hσ : IsSignotope N σ) :
    ∀ {l : List ℕ}, Chain σ t l → (∀ p ∈ l, p < N) → AllTriples σ t l
  | [], _, _ => by intro p hp; simp at hp
  | [a], _, _ => by
      intro p hp q hq r hr hpq hqr
      simp only [List.mem_singleton] at hp hq hr
      omega
  | [a, b], _, _ => by
      intro p hp q hq r hr hpq hqr
      simp only [List.mem_cons, List.not_mem_nil, or_false] at hp hq hr
      omega
  | a :: b :: c :: m, h, hN => by
      have ih := Chain.allTriples hσ h.2.2 (fun p hp => hN p (List.mem_cons_of_mem _ hp))
      have hlt := Chain.head_lt h
      have hlt' := Chain.head_lt h.2.2
      have hbc : b < c := hlt' c (by simp)
      have s1 : ∀ r ∈ c :: m, σ a b r = t := by
        intro r hr
        rcases List.mem_cons.1 hr with rfl | hr'
        · exact h.2.1
        · have hcr : c < r := Chain.head_lt h.2.2.tail r hr'
          have hbcr : σ b c r = t :=
            ih b (by simp) c (by simp) r (by simp [hr']) hbc hcr
          have hp := hσ a b c r h.1 hbc hcr (hN r (by simp [hr']))
          exact (pv_outer hp (h.2.1.trans hbcr.symm)).1.trans h.2.1
      intro p hp q hq r hr hpq hqr
      rcases List.mem_cons.1 hp with rfl | hp'
      · have hq' : q ∈ b :: c :: m := (List.mem_cons.1 hq).resolve_left (by omega)
        have hr' : r ∈ b :: c :: m := (List.mem_cons.1 hr).resolve_left (by omega)
        rcases List.mem_cons.1 hq' with rfl | hq''
        · exact s1 r ((List.mem_cons.1 hr').resolve_left (by omega))
        · have hbq : b < q := hlt' q hq''
          have habq := s1 q hq''
          have hbqr := ih b (by simp) q hq' r hr' hbq hqr
          have hp := hσ p b q r h.1 hbq hqr (hN r hr)
          exact (pv_outer hp (habq.trans hbqr.symm)).2.trans habq
      · have hq' : q ∈ b :: c :: m := (List.mem_cons.1 hq).resolve_left (by
          have := hlt p hp'
          omega)
        have hr' : r ∈ b :: c :: m := (List.mem_cons.1 hr).resolve_left (by
          have := hlt p hp'
          omega)
        exact ih p hp' q hq' r hr' hpq hqr

/-! ### The semantics of the auxiliary variables -/

/-- Semantics of Python's `V[(x,a,b,r)]`: an `r`-point chain of sign `t` starts at `x` and
ends with `a, b`. -/
def ChainEnd (σ : Sig) (t : Bool) (x a b : ℕ) : ℕ → Prop
  | 0 => False
  | 1 => False
  | 2 => False
  | 3 => x < a ∧ a < b ∧ σ x a b = t
  | r + 4 => a < b ∧ ∃ w, ChainEnd σ t x w a (r + 3) ∧ σ w a b = t

/-- Semantics of Python's `E[(x,b,r)]`: an `r`-point chain of sign `t` runs from `x` to `b`. -/
def ChainE (σ : Sig) (t : Bool) (x b r : ℕ) : Prop := ∃ a, ChainEnd σ t x a b r

theorem ChainEnd.lt : ∀ {x a b r : ℕ}, ChainEnd σ t x a b r → x < a ∧ a < b
  | _, _, _, 0, h => h.elim
  | _, _, _, 1, h => h.elim
  | _, _, _, 2, h => h.elim
  | _, _, _, 3, h => ⟨h.1, h.2.1⟩
  | _, _, _, _ + 4, ⟨hab, _, hw, _⟩ => ⟨lt_trans (ChainEnd.lt hw).1 (ChainEnd.lt hw).2, hab⟩

/-- Monotonicity: deleting the second point of an `(r+1)`-chain leaves an `r`-chain with the
same ends. -/
theorem ChainEnd.pred (hσ : IsSignotope N σ) :
    ∀ {r x a b : ℕ}, 3 ≤ r → b < N → ChainEnd σ t x a b (r + 1) → ChainEnd σ t x a b r
  | 0, _, _, _, hr, _, _ => by omega
  | 1, _, _, _, hr, _, _ => by omega
  | 2, _, _, _, hr, _, _ => by omega
  | 3, x, a, b, _, hb, ⟨hab, w, ⟨hxw, hwa, hxwa⟩, hwab⟩ => by
      have hp := hσ x w a b hxw hwa hab hb
      exact ⟨lt_trans hxw hwa, hab, (pv_outer hp (hxwa.trans hwab.symm)).2.trans hxwa⟩
  | r + 4, x, a, b, _, hb, ⟨hab, w, hw, hwab⟩ =>
      ⟨hab, w, ChainEnd.pred hσ (by omega) (lt_trans hab hb) hw, hwab⟩

theorem ChainE.pred (hσ : IsSignotope N σ) {r x b : ℕ} (hr : 3 ≤ r) (hb : b < N)
    (h : ChainE σ t x b (r + 1)) : ChainE σ t x b r :=
  let ⟨a, ha⟩ := h
  ⟨a, ChainEnd.pred hσ hr hb ha⟩

/-- The chain behind `ChainEnd`. -/
theorem ChainEnd.toList : ∀ {x a b r : ℕ}, ChainEnd σ t x a b r →
    ∃ m : List ℕ, m.length + 3 = r ∧ (∀ p ∈ m, p < a) ∧ x < a ∧ a < b ∧
      Chain σ t (x :: m ++ [a, b])
  | _, _, _, 0, h => h.elim
  | _, _, _, 1, h => h.elim
  | _, _, _, 2, h => h.elim
  | x, a, b, 3, ⟨hxa, hab, hxab⟩ => ⟨[], rfl, by simp, hxa, hab, ⟨hxa, hxab, hab⟩⟩
  | x, a, b, r + 4, ⟨hab, w, hw, hwab⟩ => by
      obtain ⟨m, hm, hmw, hxw, hwa, hc⟩ := ChainEnd.toList hw
      refine ⟨m ++ [w], by simp; omega, ?_, lt_trans hxw hwa, hab, ?_⟩
      · intro p hp
        simp only [List.mem_append, List.mem_singleton] at hp
        rcases hp with hp | rfl
        · exact lt_trans (hmw p hp) hwa
        · exact hwa
      · have := Chain.snoc (x :: m) (by simpa using hc) hab hwab
        simpa using this

theorem ChainEnd.hasChain {x a b r : ℕ} (h : ChainEnd σ t x a b r) (hb : b < N) :
    HasChain σ N t r := by
  obtain ⟨m, hm, hma, hxa, hab, hc⟩ := h.toList
  refine ⟨x :: m ++ [a, b], by simp; omega, ?_, hc⟩
  intro p hp
  simp only [List.cons_append, List.mem_cons, List.mem_append, List.not_mem_nil,
    or_false] at hp
  rcases hp with rfl | hp | rfl | rfl
  · omega
  · have := hma p hp
    omega
  · omega
  · exact hb

theorem getLast?_chain (x : ℕ) (m : List ℕ) (a b : ℕ) :
    (x :: m ++ [a, b]).getLast? = some b := by
  rw [List.getLast?_eq_getLast (by simp)]
  simp

/-- Two chain ends with the same endpoints give a gon. -/
theorem hasGon_of_chainE {x b r s K : ℕ} (hcap : ChainE σ false x b r)
    (hcup : ChainE σ true x b s) (hb : b < N) (hK : r + s = K + 2) : HasGon σ N K := by
  obtain ⟨a₁, h₁⟩ := hcap
  obtain ⟨a₂, h₂⟩ := hcup
  obtain ⟨m₁, hm₁, hma₁, hxa₁, hab₁, hc₁⟩ := h₁.toList
  obtain ⟨m₂, hm₂, hma₂, hxa₂, hab₂, hc₂⟩ := h₂.toList
  have bound : ∀ {m : List ℕ} {a : ℕ}, (∀ p ∈ m, p < a) → x < a → a < b →
      ∀ p ∈ x :: m ++ [a, b], p < N := by
    intro m a hma hxa hab p hp
    simp only [List.cons_append, List.mem_cons, List.mem_append, List.not_mem_nil,
      or_false] at hp
    rcases hp with rfl | hp | rfl | rfl
    · omega
    · have := hma p hp
      omega
    · omega
    · exact hb
  refine ⟨x :: m₁ ++ [a₁, b], x :: m₂ ++ [a₂, b], hc₁, hc₂, by simp, by simp, by simp,
    by rw [getLast?_chain, getLast?_chain], by simp; omega, bound hma₁ hxa₁ hab₁,
    bound hma₂ hxa₂ hab₂⟩

end ETV
