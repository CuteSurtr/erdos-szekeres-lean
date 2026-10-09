/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891. MIT, copyright (c) 2026 Michael Schroeder.
See docs/SCHROEDER-MIT.txt. Changes: local namespaces and Lean 4.24 APIs.
-/
import ErdosSzekeres.Omission.ResidualDomains

namespace ErdosSzekeres.Omission.BlockCompression
open StateInterface Domains ResidualDomains

/-- A finite compression certificate. Every allowed actual cell maps into
{1,2}. Membership in the shared middle state certifies strict cap growth. -/
structure Block where
  rowId : Nat
  support : List Nat
  thresholds : List Nat
  active : List Label
  deriving Repr

def compress (b : Block) (z : Label) : Nat :=
  if z.1≤b.thresholds.getD (z.2-1) 0 then 1 else 2

theorem compress_bounds (b : Block) (z : Label) : 1≤compress b z ∧ compress b z≤2 := by
  unfold compress; split_ifs <;> omega

def pairsOK (b : Block) : Bool := b.support.all (fun a=>b.support.all (fun d=>ResidualDomains.grid.all
  (fun z=>decide (Contains (ResidualDomains.shape d) z ∧ ¬Contains (ResidualDomains.shape a) z → z∈b.active))))

def growthOK (b : Block) : Bool := b.support.all (fun a=>b.active.all (fun z=>b.active.all
  (fun w=>decide (Contains (ResidualDomains.shape a) z ∧ ¬Contains (ResidualDomains.shape a) w ∧ z.1<w.1 → compress b z<compress b w))))

theorem pair_active (b : Block) (ok : pairsOK b=true) (a d : Nat)
    (ha : a∈b.support) (hd : d∈b.support) (z : Label)
    (bounds : 1≤z.1 ∧ z.1≤4 ∧ 1≤z.2 ∧ z.2≤6)
    (difference : Contains (ResidualDomains.shape d) z ∧ ¬Contains (ResidualDomains.shape a) z) : z∈b.active := by
  have h := List.all_eq_true.mp (List.all_eq_true.mp (List.all_eq_true.mp ok a ha) d hd)
    z (ResidualDomains.mem_grid z bounds)
  exact of_decide_eq_true h difference

theorem compressed_growth (b : Block) (ok : growthOK b=true) (a : Nat) (ha : a∈b.support)
    (z w : Label) (hz : z∈b.active) (hw : w∈b.active)
    (middle : Contains (ResidualDomains.shape a) z ∧ ¬Contains (ResidualDomains.shape a) w) (growth : z.1<w.1) :
    compress b z<compress b w := by
  have h := List.all_eq_true.mp (List.all_eq_true.mp (List.all_eq_true.mp ok a ha) z hz) w hw
  exact of_decide_eq_true h ⟨middle.1,middle.2,growth⟩

/-- A rank taking only the values 1 and 2 cannot support the three edges of
an actual four-cap. This is a finite chain argument, not a longest-rank claim. -/
theorem no_four_cap_of_rank2 (cup : Nat→Nat→Nat→Bool) (S : Finset Nat) (r : Nat→Nat→Nat)
    (bounds : ∀ u∈S, ∀ v∈S, u<v → 1≤r u v ∧ r u v≤2)
    (growth : ∀ u∈S, ∀ v∈S, ∀ w∈S, u<v → v<w → cup u v w=false → r u v<r v w) :
    ¬(ActualRanks.colorConfig cup true).HasNCap 4 S := by
  rintro ⟨xs,⟨chain,len⟩,inside⟩
  obtain ⟨u,v,w,x,rfl⟩ := List.length_eq_four.mp len
  have hu := inside u (by simp)
  have hv := inside v (by simp)
  have hw := inside w (by simp)
  have hx := inside x (by simp)
  have sorted := chain.1
  simp only [List.isChain_cons_cons,List.isChain_singleton,and_true] at sorted
  have signs := chain.2
  rw [List.chain3'_cons,List.chain3'_cons] at signs
  have first : cup u v w=false := by
    have hn := signs.1
    change ¬cup u v w=true at hn
    cases he : cup u v w <;> simp_all
  have second : cup v w x=false := by
    have hn := signs.2.1
    change ¬cup v w x=true at hn
    cases he : cup v w x <;> simp_all
  have g1 := growth u hu v hv w hw sorted.1 sorted.2.1 first
  have g2 := growth v hv w hw x hx sorted.2.1 sorted.2.2 second
  have lo := bounds u hu v hv sorted.1
  have hi := bounds w hw x hx sorted.2.2
  omega

end ErdosSzekeres.Omission.BlockCompression
