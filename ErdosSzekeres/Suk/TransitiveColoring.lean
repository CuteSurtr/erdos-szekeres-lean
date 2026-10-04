import ErdosSzekeres.Vendor.ETV.Main.CapCup
import Mathlib.Data.List.Triplewise

namespace ErdosSzekeres.Suk

/-- Transitivity for one color, as in Suk's Theorem 2.3. Both a color and its
complement must have this property in a transitive two-coloring. -/
def TripleTransitive {α : Type*} [LT α] (R : α → α → α → Prop) : Prop :=
  ∀ a b c d, a < b → b < c → c < d → R a b c → R b c d → R a b d ∧ R a c d

/-- For a transitive color, a monochromatic consecutive-triple path is a clique. -/
theorem transitive_path_clique {n : ℕ} (R : Fin n → Fin n → Fin n → Prop)
    (htrans : TripleTransitive R)
    (hpath : ∀ i (h : i + 2 < n),
      R ⟨i, by omega⟩ ⟨i + 1, by omega⟩ ⟨i + 2, h⟩) :
    ∀ i j k, i < j → j < k → R i j k := by
  suffices h : ∀ d : ℕ, ∀ i j k : Fin n, k.val - i.val = d →
      i < j → j < k → R i j k by
    intro i j k hij hjk
    exact h _ i j k rfl hij hjk
  intro d
  induction d using Nat.strong_induction_on with
  | h d ih =>
    intro i j k hd hij hjk
    have hi := i.isLt
    have hj := j.isLt
    have hk := k.isLt
    have hij' : i.val < j.val := hij
    have hjk' : j.val < k.val := hjk
    by_cases hjnext : j.val = i.val + 1
    · by_cases hknext : k.val = j.val + 1
      · convert hpath i.val (by omega) using 1 <;> apply Fin.ext <;> simp_all
      · let m : Fin n := ⟨k.val - 1, by omega⟩
        have hm : m.val = k.val - 1 := rfl
        have hjm : j < m := by change j.val < m.val; omega
        have hmk : m < k := by change m.val < k.val; omega
        exact (htrans i j m k hij hjm hmk
          (ih (m.val - i.val) (by omega) i j m rfl hij hjm)
          (ih (k.val - j.val) (by omega) j m k rfl hjm hmk)).1
    · let m : Fin n := ⟨j.val - 1, by omega⟩
      have hm : m.val = j.val - 1 := rfl
      have him : i < m := by change i.val < m.val; omega
      have hmj : m < j := by change m.val < j.val; omega
      exact (htrans i m j k him hmj hjk
        (ih (j.val - i.val) (by omega) i m j rfl him hmj)
        (ih (k.val - m.val) (by omega) m j k rfl hmj hjk)).2

private theorem chain3_getElem {α : Type*} {R : α → α → α → Prop}
    {l : List α} (h : l.Chain3' R) (i : ℕ) (hi : i + 2 < l.length) :
    R l[i] l[i + 1] l[i + 2] := by
  induction i generalizing l with
  | zero =>
    obtain ⟨a, b, c, l, rfl⟩ := List.takeHead3 (show 3 ≤ l.length by omega)
    exact (List.chain3'_cons.mp h).1
  | succ i ih =>
    cases l with
    | nil => simp at hi
    | cons a l =>
      have ht := h.tail
      have hi' : i + 2 < l.length := by simp only [List.length_cons] at hi; omega
      simpa [Nat.add_assoc] using ih ht hi'

theorem triplewise_of_chain3 {α : Type*} [LinearOrder α]
    {R : α → α → α → Prop} (htrans : TripleTransitive R) {l : List α}
    (hs : l.IsChain (· < ·)) (hc : l.Chain3' R) : l.Triplewise R := by
  have hmono : StrictMono l.get := fun _ _ hij => List.Sorted.rel_get_of_lt hs.pairwise hij
  have ht : TripleTransitive (fun i j k : Fin l.length => R (l.get i) (l.get j) (l.get k)) :=
    fun a b c d hab hbc hcd => htrans _ _ _ _ (hmono hab) (hmono hbc) (hmono hcd)
  have hp := transitive_path_clique _ ht (fun i hi => chain3_getElem hc i hi)
  rw [List.triplewise_iff_getElem]
  intro i j k hij hjk hk
  exact hp ⟨i, by omega⟩ ⟨j, by omega⟩ ⟨k, hk⟩ hij hjk

/-- An actual set of n distinct vertices, all increasing triples in one color. -/
def HasTripleClique {α : Type*} [LinearOrder α] (R : α → α → α → Prop)
    (n : ℕ) (s : Finset α) : Prop :=
  ∃ t ⊆ s, t.card = n ∧ ∀ a ∈ t, ∀ b ∈ t, ∀ c ∈ t, a < b → b < c → R a b c

private theorem hasTripleClique_of_list {α : Type*} [LinearOrder α]
    {R : α → α → α → Prop} {l : List α} {s : Finset α} {n : ℕ}
    (hs : l.IsChain (· < ·)) (hn : l.length = n) (hsub : l.In s)
    (hc : l.Triplewise R) : HasTripleClique R n s := by
  refine ⟨l.toFinset, ?_, ?_, ?_⟩
  · intro a ha
    exact hsub a (List.mem_toFinset.mp ha)
  · simpa [List.toFinset_card_of_nodup hs.pairwise.nodup] using hn
  · intro a ha b hb c hc' hab hbc
    obtain ⟨i, rfl⟩ := List.mem_iff_get.mp (List.mem_toFinset.mp ha)
    obtain ⟨j, rfl⟩ := List.mem_iff_get.mp (List.mem_toFinset.mp hb)
    obtain ⟨k, rfl⟩ := List.mem_iff_get.mp (List.mem_toFinset.mp hc')
    have hm : StrictMono l.get := fun _ _ hij => List.Sorted.rel_get_of_lt hs.pairwise hij
    have hij : i < j := hm.lt_iff_lt.mp hab
    have hjk : j < k := hm.lt_iff_lt.mp hbc
    exact List.triplewise_iff_getElem.mp hc i.val j.val k.val hij hjk k.isLt

/-- Upper-bound direction of Suk's Theorem 2.3. The lower-bound construction is
not needed for Suk's proof and is not asserted here. The path extraction uses
Baek's attributed cups-caps proof; transitivity upgrades its paths to cliques. -/
theorem transitive_cups_caps {α : Type*} [LinearOrder α]
    (R : α → α → α → Prop) (hR : TripleTransitive R)
    (hnotR : TripleTransitive (fun a b c => ¬ R a b c))
    (a b : ℕ) (s : Finset α) (hcard : (a + b).choose a < s.card) :
    HasTripleClique R (a + 2) s ∨ HasTripleClique (fun x y z => ¬ R x y z) (b + 2) s := by
  classical
  let C : Config α := ⟨fun x y z => ¬ R x y z, inferInstance⟩
  rcases C.cap_cup a b s hcard with ⟨l, ⟨⟨hs, hc⟩, hn⟩, hsub⟩ |
      ⟨l, ⟨⟨hs, hc⟩, hn⟩, hsub⟩
  · left
    have hc' : l.Chain3' R := by
      change l.Chain3' (fun x y z => ¬ ¬ R x y z) at hc
      simpa only [not_not] using hc
    exact hasTripleClique_of_list hs hn hsub (triplewise_of_chain3 hR hs hc')
  · right
    exact hasTripleClique_of_list hs hn hsub (triplewise_of_chain3 hnotR hs hc)

end ErdosSzekeres.Suk
