import ErdosSzekeres.Omission.ResidualDomains

namespace ErdosSzekeres.Omission.ResidualDomains

open StateInterface Domains

/-- All possible positive pair labels in the directed difference of two profiles. -/
def difference (a b : List ℕ) : Finset Label :=
  grid.toFinset.filter (fun z => Contains b z ∧ ¬ Contains a z)

/-- Compute a box directly from its finite difference. Its validity is proved
uniformly, so no external table of 23,716 boxes needs to be trusted or checked. -/
def boundingBox (a b : List ℕ) : Box :=
  let s := difference a b
  if h : s.Nonempty then
    ⟨true, s.inf' h Prod.fst, s.sup Prod.fst, s.inf' h Prod.snd, s.sup Prod.snd⟩
  else ⟨false, 0, 0, 0, 0⟩

theorem fits_boundingBox (a b : List ℕ) (z : Label) (hz : z ∈ grid)
    (hd : Contains b z ∧ ¬ Contains a z) : Fits (boundingBox a b) z := by
  have hm : z ∈ difference a b :=
    Finset.mem_filter.mpr ⟨List.mem_toFinset.mpr hz, hd⟩
  have hn : (difference a b).Nonempty := ⟨z, hm⟩
  simp only [boundingBox, dif_pos hn, Fits]
  exact ⟨trivial, Finset.inf'_le Prod.fst hm, Finset.le_sup hm,
    Finset.inf'_le Prod.snd hm, Finset.le_sup hm⟩

theorem boundingBox_valid (a b : List ℕ) : valid a b (boundingBox a b) = true := by
  apply List.all_eq_true.mpr
  intro z hz
  exact decide_eq_true (fits_boundingBox a b z hz)

def computedTable (a b : ℕ) : Box := boundingBox (shape a) (shape b)

theorem computedTable_valid (a b : ℕ) :
    valid (shape a) (shape b) (computedTable a b) = true :=
  boundingBox_valid _ _

end ErdosSzekeres.Omission.ResidualDomains
