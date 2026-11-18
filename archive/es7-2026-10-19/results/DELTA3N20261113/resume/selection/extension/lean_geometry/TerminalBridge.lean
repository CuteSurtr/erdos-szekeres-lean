import FiniteModel
import Terminal15Boolean

namespace Delta3.Balanced15

theorem not_three {P Q R : Prop} (h : P → Q → R → False) : ¬P ∨ ¬Q ∨ ¬R :=
  (Classical.em P).elim
    (fun hp => (Classical.em Q).elim
      (fun hq => Or.inr (Or.inr (fun hr => h hp hq hr)))
      (fun hq => Or.inr (Or.inl hq)))
    (fun hp => Or.inl hp)

/-- No chosen index set satisfies both exact finite determinant predicates.
This statement has no unformalized real-convexity hypothesis or conclusion. -/
theorem terminal_selection_contradiction (A : Index → Prop)
    (hT : TerminalSafe A) (hH : HitsSix A) : False := by
  have c052 : ¬A 0 ∨ ¬A 1 ∨ ¬A 6 :=
    not_three fun ha hb hc => by
      have ht := hT 0 1 6 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 1 6 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c053 : ¬A 0 ∨ ¬A 1 ∨ ¬A 7 :=
    not_three fun ha hb hc => by
      have ht := hT 0 1 7 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 1 7 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c054 : ¬A 0 ∨ ¬A 1 ∨ ¬A 8 :=
    not_three fun ha hb hc => by
      have ht := hT 0 1 8 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 1 8 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c055 : ¬A 0 ∨ ¬A 1 ∨ ¬A 9 :=
    not_three fun ha hb hc => by
      have ht := hT 0 1 9 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 1 9 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c056 : ¬A 0 ∨ ¬A 1 ∨ ¬A 11 :=
    not_three fun ha hb hc => by
      have ht := hT 0 1 11 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 1 11 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c057 : ¬A 0 ∨ ¬A 1 ∨ ¬A 12 :=
    not_three fun ha hb hc => by
      have ht := hT 0 1 12 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 1 12 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c058 : ¬A 0 ∨ ¬A 5 ∨ ¬A 6 :=
    not_three fun ha hb hc => by
      have ht := hT 0 5 6 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 6 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c059 : ¬A 0 ∨ ¬A 5 ∨ ¬A 7 :=
    not_three fun ha hb hc => by
      have ht := hT 0 5 7 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 7 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c060 : ¬A 0 ∨ ¬A 5 ∨ ¬A 8 :=
    not_three fun ha hb hc => by
      have ht := hT 0 5 8 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 8 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c061 : ¬A 0 ∨ ¬A 5 ∨ ¬A 9 :=
    not_three fun ha hb hc => by
      have ht := hT 0 5 9 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 9 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c062 : ¬A 0 ∨ ¬A 5 ∨ ¬A 11 :=
    not_three fun ha hb hc => by
      have ht := hT 0 5 11 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 11 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c064 : ¬A 0 ∨ ¬A 5 ∨ ¬A 13 :=
    not_three fun ha hb hc => by
      have ht := hT 0 5 13 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 13 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c065 : ¬A 1 ∨ ¬A 5 ∨ ¬A 6 :=
    not_three fun ha hb hc => by
      have ht := hT 1 5 6 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 6 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c066 : ¬A 1 ∨ ¬A 5 ∨ ¬A 7 :=
    not_three fun ha hb hc => by
      have ht := hT 1 5 7 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 7 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c067 : ¬A 1 ∨ ¬A 5 ∨ ¬A 8 :=
    not_three fun ha hb hc => by
      have ht := hT 1 5 8 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 8 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c068 : ¬A 1 ∨ ¬A 5 ∨ ¬A 9 :=
    not_three fun ha hb hc => by
      have ht := hT 1 5 9 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 9 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c069 : ¬A 1 ∨ ¬A 5 ∨ ¬A 11 :=
    not_three fun ha hb hc => by
      have ht := hT 1 5 11 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 11 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c071 : ¬A 1 ∨ ¬A 5 ∨ ¬A 13 :=
    not_three fun ha hb hc => by
      have ht := hT 1 5 13 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 13 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c073 : ¬A 2 ∨ ¬A 3 ∨ ¬A 6 :=
    not_three fun ha hb hc => by
      have ht := hT 2 3 6 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 3 6 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c074 : ¬A 2 ∨ ¬A 3 ∨ ¬A 7 :=
    not_three fun ha hb hc => by
      have ht := hT 2 3 7 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 3 7 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c075 : ¬A 2 ∨ ¬A 3 ∨ ¬A 8 :=
    not_three fun ha hb hc => by
      have ht := hT 2 3 8 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 3 8 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c076 : ¬A 2 ∨ ¬A 3 ∨ ¬A 9 :=
    not_three fun ha hb hc => by
      have ht := hT 2 3 9 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 3 9 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c077 : ¬A 2 ∨ ¬A 3 ∨ ¬A 11 :=
    not_three fun ha hb hc => by
      have ht := hT 2 3 11 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 3 11 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c079 : ¬A 2 ∨ ¬A 3 ∨ ¬A 13 :=
    not_three fun ha hb hc => by
      have ht := hT 2 3 13 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 3 13 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c101 : ¬A 4 ∨ ¬A 5 ∨ ¬A 10 :=
    not_three fun ha hb hc => by
      have ht := hT 4 5 10 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 5 10 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c109 : ¬A 4 ∨ ¬A 7 ∨ ¬A 12 :=
    not_three fun ha hb hc => by
      have ht := hT 4 7 12 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 7 12 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c110 : ¬A 4 ∨ ¬A 7 ∨ ¬A 13 :=
    not_three fun ha hb hc => by
      have ht := hT 4 7 13 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 7 13 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c112 : ¬A 4 ∨ ¬A 8 ∨ ¬A 13 :=
    not_three fun ha hb hc => by
      have ht := hT 4 8 13 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 8 13 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c113 : ¬A 4 ∨ ¬A 11 ∨ ¬A 12 :=
    not_three fun ha hb hc => by
      have ht := hT 4 11 12 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 11 12 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c114 : ¬A 4 ∨ ¬A 11 ∨ ¬A 13 :=
    not_three fun ha hb hc => by
      have ht := hT 4 11 13 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 11 13 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c115 : ¬A 6 ∨ ¬A 8 ∨ ¬A 9 :=
    not_three fun ha hb hc => by
      have ht := hT 6 8 9 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 8 9 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c122 : ¬A 7 ∨ ¬A 8 ∨ ¬A 12 :=
    not_three fun ha hb hc => by
      have ht := hT 7 8 12 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 8 12 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c123 : ¬A 7 ∨ ¬A 8 ∨ ¬A 13 :=
    not_three fun ha hb hc => by
      have ht := hT 7 8 13 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 8 13 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c124 : ¬A 7 ∨ ¬A 8 ∨ ¬A 14 :=
    not_three fun ha hb hc => by
      have ht := hT 7 8 14 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 8 14 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c125 : ¬A 7 ∨ ¬A 9 ∨ ¬A 10 :=
    not_three fun ha hb hc => by
      have ht := hT 7 9 10 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 9 10 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c126 : ¬A 7 ∨ ¬A 9 ∨ ¬A 14 :=
    not_three fun ha hb hc => by
      have ht := hT 7 9 14 (by decide +kernel) (by decide +kernel)
        (by decide +kernel) ha hb hc
      have hf : terminalPair 9 14 = false := by decide +kernel
      exact Bool.noConfusion (hf.symm.trans ht)
  have c127 : A 0 ∨ A 1 ∨ A 2 ∨ A 4 ∨ A 6 ∨ A 7 :=
    hH 0 1 2 4 6 7
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c128 : A 0 ∨ A 1 ∨ A 3 ∨ A 4 ∨ A 6 ∨ A 7 :=
    hH 0 1 3 4 6 7
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c129 : A 0 ∨ A 2 ∨ A 4 ∨ A 5 ∨ A 6 ∨ A 7 :=
    hH 0 2 4 5 6 7
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c130 : A 1 ∨ A 2 ∨ A 4 ∨ A 5 ∨ A 6 ∨ A 7 :=
    hH 1 2 4 5 6 7
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c131 : A 0 ∨ A 3 ∨ A 4 ∨ A 5 ∨ A 6 ∨ A 7 :=
    hH 0 3 4 5 6 7
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c132 : A 1 ∨ A 3 ∨ A 4 ∨ A 5 ∨ A 6 ∨ A 7 :=
    hH 1 3 4 5 6 7
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c139 : A 0 ∨ A 1 ∨ A 2 ∨ A 4 ∨ A 7 ∨ A 8 :=
    hH 0 1 2 4 7 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c140 : A 0 ∨ A 1 ∨ A 3 ∨ A 4 ∨ A 7 ∨ A 8 :=
    hH 0 1 3 4 7 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c141 : A 0 ∨ A 2 ∨ A 4 ∨ A 5 ∨ A 7 ∨ A 8 :=
    hH 0 2 4 5 7 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c142 : A 1 ∨ A 2 ∨ A 4 ∨ A 5 ∨ A 7 ∨ A 8 :=
    hH 1 2 4 5 7 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c143 : A 0 ∨ A 3 ∨ A 4 ∨ A 5 ∨ A 7 ∨ A 8 :=
    hH 0 3 4 5 7 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c144 : A 1 ∨ A 3 ∨ A 4 ∨ A 5 ∨ A 7 ∨ A 8 :=
    hH 1 3 4 5 7 8
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c151 : A 0 ∨ A 1 ∨ A 2 ∨ A 4 ∨ A 7 ∨ A 9 :=
    hH 0 1 2 4 7 9
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c152 : A 0 ∨ A 1 ∨ A 3 ∨ A 4 ∨ A 7 ∨ A 9 :=
    hH 0 1 3 4 7 9
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c153 : A 0 ∨ A 2 ∨ A 4 ∨ A 5 ∨ A 7 ∨ A 9 :=
    hH 0 2 4 5 7 9
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c154 : A 1 ∨ A 2 ∨ A 4 ∨ A 5 ∨ A 7 ∨ A 9 :=
    hH 1 2 4 5 7 9
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c155 : A 0 ∨ A 3 ∨ A 4 ∨ A 5 ∨ A 7 ∨ A 9 :=
    hH 0 3 4 5 7 9
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c156 : A 1 ∨ A 3 ∨ A 4 ∨ A 5 ∨ A 7 ∨ A 9 :=
    hH 1 3 4 5 7 9
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c157 : A 0 ∨ A 1 ∨ A 2 ∨ A 4 ∨ A 8 ∨ A 9 :=
    hH 0 1 2 4 8 9
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c158 : A 0 ∨ A 1 ∨ A 3 ∨ A 4 ∨ A 8 ∨ A 9 :=
    hH 0 1 3 4 8 9
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c159 : A 0 ∨ A 2 ∨ A 4 ∨ A 5 ∨ A 8 ∨ A 9 :=
    hH 0 2 4 5 8 9
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c160 : A 1 ∨ A 2 ∨ A 4 ∨ A 5 ∨ A 8 ∨ A 9 :=
    hH 1 2 4 5 8 9
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c161 : A 0 ∨ A 3 ∨ A 4 ∨ A 5 ∨ A 8 ∨ A 9 :=
    hH 0 3 4 5 8 9
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c162 : A 1 ∨ A 3 ∨ A 4 ∨ A 5 ∨ A 8 ∨ A 9 :=
    hH 1 3 4 5 8 9
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c184 : A 0 ∨ A 1 ∨ A 2 ∨ A 7 ∨ A 8 ∨ A 11 :=
    hH 0 1 2 7 8 11
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c185 : A 0 ∨ A 1 ∨ A 3 ∨ A 7 ∨ A 8 ∨ A 11 :=
    hH 0 1 3 7 8 11
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c186 : A 0 ∨ A 2 ∨ A 5 ∨ A 7 ∨ A 8 ∨ A 11 :=
    hH 0 2 5 7 8 11
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c187 : A 1 ∨ A 2 ∨ A 5 ∨ A 7 ∨ A 8 ∨ A 11 :=
    hH 1 2 5 7 8 11
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c188 : A 0 ∨ A 3 ∨ A 5 ∨ A 7 ∨ A 8 ∨ A 11 :=
    hH 0 3 5 7 8 11
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c189 : A 1 ∨ A 3 ∨ A 5 ∨ A 7 ∨ A 8 ∨ A 11 :=
    hH 1 3 5 7 8 11
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c214 : A 6 ∨ A 7 ∨ A 8 ∨ A 9 ∨ A 11 ∨ A 12 :=
    hH 6 7 8 9 11 12
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c227 : A 0 ∨ A 2 ∨ A 5 ∨ A 7 ∨ A 11 ∨ A 13 :=
    hH 0 2 5 7 11 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c228 : A 1 ∨ A 2 ∨ A 5 ∨ A 7 ∨ A 11 ∨ A 13 :=
    hH 1 2 5 7 11 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c229 : A 0 ∨ A 3 ∨ A 5 ∨ A 7 ∨ A 11 ∨ A 13 :=
    hH 0 3 5 7 11 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c230 : A 1 ∨ A 3 ∨ A 5 ∨ A 7 ∨ A 11 ∨ A 13 :=
    hH 1 3 5 7 11 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c231 : A 6 ∨ A 7 ∨ A 8 ∨ A 9 ∨ A 11 ∨ A 13 :=
    hH 6 7 8 9 11 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c236 : A 1 ∨ A 2 ∨ A 7 ∨ A 10 ∨ A 11 ∨ A 13 :=
    hH 1 2 7 10 11 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c238 : A 1 ∨ A 3 ∨ A 7 ∨ A 10 ∨ A 11 ∨ A 13 :=
    hH 1 3 7 10 11 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c242 : A 0 ∨ A 2 ∨ A 5 ∨ A 6 ∨ A 12 ∨ A 13 :=
    hH 0 2 5 6 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c243 : A 1 ∨ A 2 ∨ A 5 ∨ A 6 ∨ A 12 ∨ A 13 :=
    hH 1 2 5 6 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c244 : A 0 ∨ A 3 ∨ A 5 ∨ A 6 ∨ A 12 ∨ A 13 :=
    hH 0 3 5 6 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c245 : A 1 ∨ A 3 ∨ A 5 ∨ A 6 ∨ A 12 ∨ A 13 :=
    hH 1 3 5 6 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c246 : A 0 ∨ A 2 ∨ A 5 ∨ A 8 ∨ A 12 ∨ A 13 :=
    hH 0 2 5 8 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c247 : A 1 ∨ A 2 ∨ A 5 ∨ A 8 ∨ A 12 ∨ A 13 :=
    hH 1 2 5 8 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c248 : A 0 ∨ A 3 ∨ A 5 ∨ A 8 ∨ A 12 ∨ A 13 :=
    hH 0 3 5 8 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c249 : A 1 ∨ A 3 ∨ A 5 ∨ A 8 ∨ A 12 ∨ A 13 :=
    hH 1 3 5 8 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c250 : A 0 ∨ A 2 ∨ A 5 ∨ A 9 ∨ A 12 ∨ A 13 :=
    hH 0 2 5 9 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c251 : A 1 ∨ A 2 ∨ A 5 ∨ A 9 ∨ A 12 ∨ A 13 :=
    hH 1 2 5 9 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c252 : A 0 ∨ A 3 ∨ A 5 ∨ A 9 ∨ A 12 ∨ A 13 :=
    hH 0 3 5 9 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c253 : A 1 ∨ A 3 ∨ A 5 ∨ A 9 ∨ A 12 ∨ A 13 :=
    hH 1 3 5 9 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c255 : A 1 ∨ A 2 ∨ A 6 ∨ A 10 ∨ A 12 ∨ A 13 :=
    hH 1 2 6 10 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c257 : A 1 ∨ A 3 ∨ A 6 ∨ A 10 ∨ A 12 ∨ A 13 :=
    hH 1 3 6 10 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c261 : A 1 ∨ A 2 ∨ A 8 ∨ A 10 ∨ A 12 ∨ A 13 :=
    hH 1 2 8 10 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c263 : A 1 ∨ A 3 ∨ A 8 ∨ A 10 ∨ A 12 ∨ A 13 :=
    hH 1 3 8 10 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c267 : A 1 ∨ A 2 ∨ A 9 ∨ A 10 ∨ A 12 ∨ A 13 :=
    hH 1 2 9 10 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c269 : A 1 ∨ A 3 ∨ A 9 ∨ A 10 ∨ A 12 ∨ A 13 :=
    hH 1 3 9 10 12 13
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c280 : A 0 ∨ A 2 ∨ A 4 ∨ A 8 ∨ A 10 ∨ A 14 :=
    hH 0 2 4 8 10 14
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c281 : A 1 ∨ A 2 ∨ A 4 ∨ A 8 ∨ A 10 ∨ A 14 :=
    hH 1 2 4 8 10 14
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c282 : A 0 ∨ A 3 ∨ A 4 ∨ A 8 ∨ A 10 ∨ A 14 :=
    hH 0 3 4 8 10 14
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c283 : A 1 ∨ A 3 ∨ A 4 ∨ A 8 ∨ A 10 ∨ A 14 :=
    hH 1 3 4 8 10 14
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c311 : A 1 ∨ A 2 ∨ A 9 ∨ A 12 ∨ A 13 ∨ A 14 :=
    hH 1 2 9 12 13 14
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  have c313 : A 1 ∨ A 3 ∨ A 9 ∨ A 12 ∨ A 13 ∨ A 14 :=
    hH 1 3 9 12 13 14
      (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel) (by decide +kernel)
  exact Delta3.Terminal15Boolean.core_unsat
    (A 0) (A 1) (A 2) (A 3) (A 4) (A 5) (A 6) (A 7) (A 8) (A 9) (A 10) (A 11) (A 12) (A 13) (A 14)
    c052 c053 c054 c055 c056 c057 c058 c059 c060 c061 c062 c064 c065 c066 c067 c068 c069 c071 c073 c074 c075 c076 c077 c079 c101 c109 c110 c112 c113 c114 c115 c122 c123 c124 c125 c126 c127 c128 c129 c130 c131 c132 c139 c140 c141 c142 c143 c144 c151 c152 c153 c154 c155 c156 c157 c158 c159 c160 c161 c162 c184 c185 c186 c187 c188 c189 c214 c227 c228 c229 c230 c231 c236 c238 c242 c243 c244 c245 c246 c247 c248 c249 c250 c251 c252 c253 c255 c257 c261 c263 c267 c269 c280 c281 c282 c283 c311 c313

theorem no_terminal_selection : ¬∃ A : Index → Prop, TerminalSafe A ∧ HitsSix A :=
  fun ⟨A, hT, hH⟩ => terminal_selection_contradiction A hT hH

theorem no_boolean_terminal_selection :
    ¬∃ A : Index → Bool, TerminalSafe (fun i => A i = true) ∧ HitsSix (fun i => A i = true) :=
  fun ⟨A, hT, hH⟩ => terminal_selection_contradiction (fun i => A i = true) hT hH

#print axioms not_three
#print axioms terminal_selection_contradiction
#print axioms no_terminal_selection
#print axioms no_boolean_terminal_selection

end Delta3.Balanced15
