import T12FiniteModel
import T12Boolean

namespace Delta3.Terminal12

theorem not_three {P Q R : Prop} (h : P → Q → R → False) : ¬P ∨ ¬Q ∨ ¬R :=
  (Classical.em P).elim
    (fun hp => (Classical.em Q).elim
      (fun hq => Or.inr (Or.inr (fun hr => h hp hq hr)))
      (fun hq => Or.inr (Or.inl hq)))
    (fun hp => Or.inl hp)

/-- No chosen index set satisfies both exact finite determinant predicates.
This statement has no unformalized real-convexity hypothesis or conclusion. -/
theorem terminal_selection_contradiction (A : Index → Prop)
    (hT : TerminalSafe A) (hH : HitsFive A) : False := by
  have c017 : ¬A 0 ∨ ¬A 1 ∨ ¬A 5 :=
    not_three fun ha hb hc => by
      have ht := hT 0 1 5 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 1 5 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c018 : ¬A 0 ∨ ¬A 1 ∨ ¬A 6 :=
    not_three fun ha hb hc => by
      have ht := hT 0 1 6 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 1 6 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c019 : ¬A 0 ∨ ¬A 1 ∨ ¬A 7 :=
    not_three fun ha hb hc => by
      have ht := hT 0 1 7 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 1 7 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c020 : ¬A 0 ∨ ¬A 1 ∨ ¬A 8 :=
    not_three fun ha hb hc => by
      have ht := hT 0 1 8 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 1 8 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c021 : ¬A 0 ∨ ¬A 1 ∨ ¬A 10 :=
    not_three fun ha hb hc => by
      have ht := hT 0 1 10 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 1 10 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c022 : ¬A 0 ∨ ¬A 4 ∨ ¬A 5 :=
    not_three fun ha hb hc => by
      have ht := hT 0 4 5 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 4 5 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c023 : ¬A 0 ∨ ¬A 4 ∨ ¬A 6 :=
    not_three fun ha hb hc => by
      have ht := hT 0 4 6 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 4 6 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c024 : ¬A 0 ∨ ¬A 4 ∨ ¬A 7 :=
    not_three fun ha hb hc => by
      have ht := hT 0 4 7 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 4 7 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c025 : ¬A 0 ∨ ¬A 4 ∨ ¬A 8 :=
    not_three fun ha hb hc => by
      have ht := hT 0 4 8 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 4 8 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c026 : ¬A 0 ∨ ¬A 4 ∨ ¬A 10 :=
    not_three fun ha hb hc => by
      have ht := hT 0 4 10 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 4 10 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c027 : ¬A 1 ∨ ¬A 4 ∨ ¬A 5 :=
    not_three fun ha hb hc => by
      have ht := hT 1 4 5 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 4 5 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c028 : ¬A 1 ∨ ¬A 4 ∨ ¬A 6 :=
    not_three fun ha hb hc => by
      have ht := hT 1 4 6 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 4 6 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c029 : ¬A 1 ∨ ¬A 4 ∨ ¬A 7 :=
    not_three fun ha hb hc => by
      have ht := hT 1 4 7 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 4 7 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c030 : ¬A 1 ∨ ¬A 4 ∨ ¬A 8 :=
    not_three fun ha hb hc => by
      have ht := hT 1 4 8 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 4 8 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c031 : ¬A 1 ∨ ¬A 4 ∨ ¬A 10 :=
    not_three fun ha hb hc => by
      have ht := hT 1 4 10 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 4 10 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c032 : ¬A 2 ∨ ¬A 3 ∨ ¬A 5 :=
    not_three fun ha hb hc => by
      have ht := hT 2 3 5 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 3 5 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c033 : ¬A 2 ∨ ¬A 3 ∨ ¬A 6 :=
    not_three fun ha hb hc => by
      have ht := hT 2 3 6 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 3 6 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c034 : ¬A 2 ∨ ¬A 3 ∨ ¬A 7 :=
    not_three fun ha hb hc => by
      have ht := hT 2 3 7 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 3 7 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c035 : ¬A 2 ∨ ¬A 3 ∨ ¬A 8 :=
    not_three fun ha hb hc => by
      have ht := hT 2 3 8 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 3 8 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c036 : ¬A 2 ∨ ¬A 3 ∨ ¬A 10 :=
    not_three fun ha hb hc => by
      have ht := hT 2 3 10 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 3 10 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c051 : ¬A 5 ∨ ¬A 7 ∨ ¬A 10 :=
    not_three fun ha hb hc => by
      have ht := hT 5 7 10 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 7 10 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c053 : ¬A 6 ∨ ¬A 7 ∨ ¬A 8 :=
    not_three fun ha hb hc => by
      have ht := hT 6 7 8 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 7 8 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c057 : ¬A 6 ∨ ¬A 8 ∨ ¬A 9 :=
    not_three fun ha hb hc => by
      have ht := hT 6 8 9 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 8 9 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c058 : ¬A 6 ∨ ¬A 8 ∨ ¬A 11 :=
    not_three fun ha hb hc => by
      have ht := hT 6 8 11 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 8 11 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c059 : A 0 ∨ A 1 ∨ A 2 ∨ A 5 ∨ A 6 :=
    hH 0 1 2 5 6
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c061 : A 0 ∨ A 1 ∨ A 2 ∨ A 5 ∨ A 8 :=
    hH 0 1 2 5 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c063 : A 0 ∨ A 1 ∨ A 2 ∨ A 6 ∨ A 7 :=
    hH 0 1 2 6 7
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c065 : A 0 ∨ A 1 ∨ A 2 ∨ A 6 ∨ A 10 :=
    hH 0 1 2 6 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c066 : A 0 ∨ A 1 ∨ A 2 ∨ A 7 ∨ A 8 :=
    hH 0 1 2 7 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c068 : A 0 ∨ A 1 ∨ A 2 ∨ A 8 ∨ A 10 :=
    hH 0 1 2 8 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c069 : A 0 ∨ A 1 ∨ A 3 ∨ A 5 ∨ A 6 :=
    hH 0 1 3 5 6
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c071 : A 0 ∨ A 1 ∨ A 3 ∨ A 5 ∨ A 8 :=
    hH 0 1 3 5 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c073 : A 0 ∨ A 1 ∨ A 3 ∨ A 6 ∨ A 7 :=
    hH 0 1 3 6 7
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c075 : A 0 ∨ A 1 ∨ A 3 ∨ A 6 ∨ A 10 :=
    hH 0 1 3 6 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c076 : A 0 ∨ A 1 ∨ A 3 ∨ A 7 ∨ A 8 :=
    hH 0 1 3 7 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c078 : A 0 ∨ A 1 ∨ A 3 ∨ A 8 ∨ A 10 :=
    hH 0 1 3 8 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c082 : A 0 ∨ A 2 ∨ A 4 ∨ A 5 ∨ A 6 :=
    hH 0 2 4 5 6
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c084 : A 0 ∨ A 2 ∨ A 4 ∨ A 5 ∨ A 8 :=
    hH 0 2 4 5 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c086 : A 0 ∨ A 2 ∨ A 4 ∨ A 6 ∨ A 7 :=
    hH 0 2 4 6 7
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c088 : A 0 ∨ A 2 ∨ A 4 ∨ A 6 ∨ A 10 :=
    hH 0 2 4 6 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c089 : A 0 ∨ A 2 ∨ A 4 ∨ A 7 ∨ A 8 :=
    hH 0 2 4 7 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c091 : A 0 ∨ A 2 ∨ A 4 ∨ A 8 ∨ A 10 :=
    hH 0 2 4 8 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c101 : A 0 ∨ A 2 ∨ A 7 ∨ A 9 ∨ A 11 :=
    hH 0 2 7 9 11
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c105 : A 0 ∨ A 3 ∨ A 4 ∨ A 5 ∨ A 6 :=
    hH 0 3 4 5 6
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c107 : A 0 ∨ A 3 ∨ A 4 ∨ A 5 ∨ A 8 :=
    hH 0 3 4 5 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c109 : A 0 ∨ A 3 ∨ A 4 ∨ A 6 ∨ A 7 :=
    hH 0 3 4 6 7
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c111 : A 0 ∨ A 3 ∨ A 4 ∨ A 6 ∨ A 10 :=
    hH 0 3 4 6 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c112 : A 0 ∨ A 3 ∨ A 4 ∨ A 7 ∨ A 8 :=
    hH 0 3 4 7 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c114 : A 0 ∨ A 3 ∨ A 4 ∨ A 8 ∨ A 10 :=
    hH 0 3 4 8 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c124 : A 0 ∨ A 3 ∨ A 7 ∨ A 9 ∨ A 11 :=
    hH 0 3 7 9 11
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c130 : A 1 ∨ A 2 ∨ A 4 ∨ A 5 ∨ A 6 :=
    hH 1 2 4 5 6
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c132 : A 1 ∨ A 2 ∨ A 4 ∨ A 5 ∨ A 8 :=
    hH 1 2 4 5 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c134 : A 1 ∨ A 2 ∨ A 4 ∨ A 6 ∨ A 7 :=
    hH 1 2 4 6 7
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c136 : A 1 ∨ A 2 ∨ A 4 ∨ A 6 ∨ A 10 :=
    hH 1 2 4 6 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c137 : A 1 ∨ A 2 ∨ A 4 ∨ A 7 ∨ A 8 :=
    hH 1 2 4 7 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c139 : A 1 ∨ A 2 ∨ A 4 ∨ A 8 ∨ A 10 :=
    hH 1 2 4 8 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c149 : A 1 ∨ A 2 ∨ A 7 ∨ A 9 ∨ A 11 :=
    hH 1 2 7 9 11
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c153 : A 1 ∨ A 3 ∨ A 4 ∨ A 5 ∨ A 6 :=
    hH 1 3 4 5 6
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c155 : A 1 ∨ A 3 ∨ A 4 ∨ A 5 ∨ A 8 :=
    hH 1 3 4 5 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c157 : A 1 ∨ A 3 ∨ A 4 ∨ A 6 ∨ A 7 :=
    hH 1 3 4 6 7
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c159 : A 1 ∨ A 3 ∨ A 4 ∨ A 6 ∨ A 10 :=
    hH 1 3 4 6 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c160 : A 1 ∨ A 3 ∨ A 4 ∨ A 7 ∨ A 8 :=
    hH 1 3 4 7 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c162 : A 1 ∨ A 3 ∨ A 4 ∨ A 8 ∨ A 10 :=
    hH 1 3 4 8 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c172 : A 1 ∨ A 3 ∨ A 7 ∨ A 9 ∨ A 11 :=
    hH 1 3 7 9 11
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c188 : A 5 ∨ A 6 ∨ A 7 ∨ A 8 ∨ A 10 :=
    hH 5 6 7 8 10
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  exact Delta3.T12Boolean.core_unsat
    (A 0) (A 1) (A 2) (A 3) (A 4) (A 5) (A 6) (A 7) (A 8) (A 9) (A 10) (A 11)
    c017 c018 c019 c020 c021 c022 c023 c024 c025 c026 c027 c028 c029 c030 c031 c032 c033 c034 c035 c036 c051 c053 c057 c058 c059 c061 c063 c065 c066 c068 c069 c071 c073 c075 c076 c078 c082 c084 c086 c088 c089 c091 c101 c105 c107 c109 c111 c112 c114 c124 c130 c132 c134 c136 c137 c139 c149 c153 c155 c157 c159 c160 c162 c172 c188

theorem no_terminal_selection : ¬∃ A : Index → Prop, TerminalSafe A ∧ HitsFive A :=
  fun ⟨A, hT, hH⟩ => terminal_selection_contradiction A hT hH

theorem no_boolean_terminal_selection :
    ¬∃ A : Index → Bool, TerminalSafe (fun i => A i = true) ∧ HitsFive (fun i => A i = true) :=
  fun ⟨A, hT, hH⟩ => terminal_selection_contradiction (fun i => A i = true) hT hH

#print axioms not_three
#print axioms terminal_selection_contradiction
#print axioms no_terminal_selection
#print axioms no_boolean_terminal_selection

end Delta3.Terminal12
