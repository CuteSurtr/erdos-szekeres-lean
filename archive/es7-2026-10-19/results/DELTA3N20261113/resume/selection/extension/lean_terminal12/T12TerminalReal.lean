import T12ConvexBridge
import T12PredicateSemantics
import T12TerminalBridge

noncomputable section

namespace Delta3.Terminal12.RealBridge

/-- A cap of real indexed points, expressed by its ordered triple orientations. -/
def RealCap (s : List Index) : Prop :=
  ∀ a b c : Index, [a, b, c].Sublist s →
    ErdosSzekeres.orient (realPoint a) (realPoint b) (realPoint c) < 0

theorem cap_real_iff (s : List Index) : cap s = true ↔ RealCap s := by
  constructor
  · intro hc a b c ht
    have hm : [a, b, c] ∈ choose 3 s := mem_choose_of_sublist ht
    have hi : det a b c < 0 := by
      simpa only [tripleCap, decide_eq_true_eq] using List.all_eq_true.mp hc [a, b, c] hm
    rw [real_orient]
    exact_mod_cast hi
  · intro hc
    apply List.all_eq_true.mpr
    intro t ht
    obtain ⟨hsub, hlen⟩ := choose_sound ht
    obtain ⟨a, b, c, rfl⟩ := List.length_eq_three.mp hlen
    have hr := hc a b c hsub
    simp only [tripleCap, decide_eq_true_eq]
    rw [real_orient] at hr
    exact_mod_cast hr

theorem no_real_five_cap_subsequence (s : List Index) (hs : s.Sublist indices)
    (hlen : s.length = 5) : ¬RealCap s :=
  fun hc => Bool.noConfusion ((five_subsequence_not_cap s hs hlen).symm.trans
    ((cap_real_iff s).mpr hc))

/-- Every selected real cap triple has an ambient real four-cap with the same last pair. -/
def RealTerminalSafe (A : Index → Prop) : Prop :=
  ∀ a b c : Index, a < b → b < c →
    ErdosSzekeres.orient (realPoint a) (realPoint b) (realPoint c) < 0 →
    A a → A b → A c →
    ∃ u v : Index, u < v ∧ v < b ∧ b < c ∧ RealCap [u, v, b, c]

/-- Hitting every real convex five-set, expressed using its increasing index order. -/
def RealHitsFive (A : Index → Prop) : Prop :=
  ∀ a b c d e : Index, a < b → b < c → c < d → d < e →
    ErdosSzekeres.ConvexPosition ([a, b, c, d, e].toFinset.image realPoint) →
      A a ∨ A b ∨ A c ∨ A d ∨ A e

theorem terminalSafe_of_real (A : Index → Prop) (h : RealTerminalSafe A) : TerminalSafe A := by
  intro a b c hab hbc hdet ha hb hc
  have hr : ErdosSzekeres.orient (realPoint a) (realPoint b) (realPoint c) < 0 := by
    rw [real_orient]
    exact_mod_cast hdet
  obtain ⟨u, v, huv, hvb, hbc', hcap⟩ := h a b c hab hbc hr ha hb hc
  exact (terminalPair_iff b c).mpr ⟨u, v, huv, hvb, hbc', (cap_real_iff _).mpr hcap⟩

theorem hitsFive_of_real (A : Index → Prop) (h : RealHitsFive A) : HitsFive A := by
  intro a b c d e hab hbc hcd hde hconv
  have hs : [a, b, c, d, e].Pairwise (· < ·) := by
    apply List.IsChain.pairwise
    simp only [List.isChain_cons_cons, List.IsChain.singleton, and_true]
    exact ⟨hab, hbc, hcd, hde⟩
  exact h a b c d e hab hbc hcd hde
    (real_of_signConvex _ hs.nodup (hs.imp (fun hlt => hlt.le)) (by simp) hconv)

theorem no_real_terminal_selection : ¬∃ A : Index → Prop, RealTerminalSafe A ∧ RealHitsFive A :=
  fun ⟨A, hT, hH⟩ => terminal_selection_contradiction A
    (terminalSafe_of_real A hT) (hitsFive_of_real A hH)

#print axioms cap_real_iff
#print axioms no_real_five_cap_subsequence
#print axioms terminalSafe_of_real
#print axioms hitsFive_of_real
#print axioms no_real_terminal_selection

end Delta3.Terminal12.RealBridge
