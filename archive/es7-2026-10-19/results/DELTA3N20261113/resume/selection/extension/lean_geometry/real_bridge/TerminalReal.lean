import ConvexBridge
import PredicateSemantics
import TerminalBridge

noncomputable section

namespace Delta3.Balanced15.RealBridge

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

/-- Hitting every real convex six-set, expressed using its increasing index order. -/
def RealHitsSix (A : Index → Prop) : Prop :=
  ∀ a b c d e f : Index, a < b → b < c → c < d → d < e → e < f →
    ErdosSzekeres.ConvexPosition ([a, b, c, d, e, f].toFinset.image realPoint) →
      A a ∨ A b ∨ A c ∨ A d ∨ A e ∨ A f

theorem terminalSafe_of_real (A : Index → Prop) (h : RealTerminalSafe A) : TerminalSafe A := by
  intro a b c hab hbc hdet ha hb hc
  have hr : ErdosSzekeres.orient (realPoint a) (realPoint b) (realPoint c) < 0 := by
    rw [real_orient]
    exact_mod_cast hdet
  obtain ⟨u, v, huv, hvb, hbc', hcap⟩ := h a b c hab hbc hr ha hb hc
  exact (terminalPair_iff b c).mpr ⟨u, v, huv, hvb, hbc', (cap_real_iff _).mpr hcap⟩

theorem hitsSix_of_real (A : Index → Prop) (h : RealHitsSix A) : HitsSix A := by
  intro a b c d e f hab hbc hcd hde hef hconv
  have hs : [a, b, c, d, e, f].Pairwise (· < ·) := by
    simp [List.pairwise_cons]
    exact ⟨⟨hab, hab.trans hbc, (hab.trans hbc).trans hcd,
        ((hab.trans hbc).trans hcd).trans hde,
        (((hab.trans hbc).trans hcd).trans hde).trans hef⟩,
      ⟨hbc, hbc.trans hcd, (hbc.trans hcd).trans hde,
        ((hbc.trans hcd).trans hde).trans hef⟩,
      ⟨hcd, hcd.trans hde, (hcd.trans hde).trans hef⟩,
      ⟨hde, hde.trans hef⟩, hef⟩
  exact h a b c d e f hab hbc hcd hde hef
    (real_of_signConvex _ hs.nodup (hs.imp (fun hlt => hlt.le)) (by simp) hconv)

theorem no_real_terminal_selection : ¬∃ A : Index → Prop, RealTerminalSafe A ∧ RealHitsSix A :=
  fun ⟨A, hT, hH⟩ => terminal_selection_contradiction A
    (terminalSafe_of_real A hT) (hitsSix_of_real A hH)

#print axioms cap_real_iff
#print axioms no_real_five_cap_subsequence
#print axioms terminalSafe_of_real
#print axioms hitsSix_of_real
#print axioms no_real_terminal_selection

end Delta3.Balanced15.RealBridge
