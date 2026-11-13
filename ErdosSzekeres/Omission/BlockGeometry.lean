/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891. MIT, copyright (c) 2026 Michael Schroeder.
See docs/SCHROEDER-MIT.txt. Changes: local namespaces and Lean 4.24 APIs.
-/
import ErdosSzekeres.Omission.BlockCompression
import ErdosSzekeres.Omission.BaekGeometry
import ErdosSzekeres.Omission.ResidualCycleGeometry

namespace ErdosSzekeres.Omission.BlockGeometry
open StateInterface Domains ResidualRanks ResidualCatalog BlockCompression

noncomputable def owners {n} (index : Fin n→Nat) (support : List Nat) : Finset (Fin n) :=
  Finset.univ.filter (fun v=>index v∈support)

noncomputable def ownerNats {n} (index : Fin n→Nat) (support : List Nat) : Finset Nat :=
  (owners index support).image Fin.val

theorem mem_owners {n} (index : Fin n→Nat) (support : List Nat) (v : Fin n) :
    v∈owners index support ↔ index v∈support := by simp [owners]

theorem member_bounded {n} (index : Fin n→Nat) (support : List Nat) (u : Nat)
    (hu : u∈ownerNats index support) : u<n := by
  obtain ⟨v,_,rfl⟩ := Finset.mem_image.mp hu
  exact v.isLt

theorem nat_mem_iff {n} (index : Fin n→Nat) (support : List Nat) (v : Fin n) :
    v.val∈ownerNats index support ↔ index v∈support := by
  constructor
  · intro h
    obtain ⟨w,hw,eq⟩ := Finset.mem_image.mp h
    have he : w=v := Fin.ext eq
    subst w
    exact (mem_owners index support v).mp hw
  · intro h
    exact Finset.mem_image.mpr ⟨v,(mem_owners index support v).mpr h,rfl⟩

theorem support_count {n} (index : Fin n→Nat) (inj : Function.Injective index) (support : List Nat) :
    (support.toFinset∩Finset.univ.image index).card=(ownerNats index support).card := by
  classical
  have image : (owners index support).image index=support.toFinset∩Finset.univ.image index := by
    ext i
    constructor
    · intro h
      obtain ⟨v,hv,rfl⟩ := Finset.mem_image.mp h
      exact Finset.mem_inter.mpr ⟨List.mem_toFinset.mpr ((mem_owners index support v).mp hv),
        Finset.mem_image.mpr ⟨v,by simp,rfl⟩⟩
    · intro h
      obtain ⟨hi,hv⟩ := Finset.mem_inter.mp h
      obtain ⟨v,_,rfl⟩ := Finset.mem_image.mp hv
      exact Finset.mem_image.mpr ⟨v,(mem_owners index support v).mpr (List.mem_toFinset.mp hi),rfl⟩
  rw [←image,Finset.card_image_of_injective _ inj]
  unfold ownerNats
  rw [Finset.card_image_of_injective _ Fin.val_injective]

/-- The selected pair's actual cell belongs to precisely the directed source
state difference. Both states are recomputed in the same residual configuration. -/
theorem pair_difference (n cup)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup)
    (u v : Fin n) (huv : u<v) :
    Contains (ResidualDomains.shape (ownerIndex n cup caps cups junction v).val) (labels n cup u v) ∧
    ¬Contains (ResidualDomains.shape (ownerIndex n cup caps cups junction u).val) (labels n cup u v) := by
  have bd := label_bounds n cup caps cups u v huv v.isLt
  rw [ResidualDomains.owner_contains n cup caps cups junction v _ bd,
    ResidualDomains.owner_contains n cup caps cups junction u _ bd]
  exact incoming_admissible n cup (labels n cup) (labels_increasing n cup caps) u v huv v.isLt

theorem actual_compressed_growth (n cup)
    (caps : ¬(ActualRanks.colorConfig cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n cup true 8) (junction : NoJunction n cup)
    (b : Block) (pairs : pairsOK b=true) (growth : growthOK b=true)
    (u v w : Fin n)
    (hu : (ownerIndex n cup caps cups junction u).val∈b.support)
    (hv : (ownerIndex n cup caps cups junction v).val∈b.support)
    (hw : (ownerIndex n cup caps cups junction w).val∈b.support)
    (uv : u<v) (vw : v<w) (cap : cup u v w=false) :
    compress b (labels n cup u v)<compress b (labels n cup v w) := by
  have uvDiff := pair_difference n cup caps cups junction u v uv
  have vwDiff := pair_difference n cup caps cups junction v w vw
  have uva := pair_active b pairs _ _ hu hv _ (label_bounds n cup caps cups u v uv v.isLt) uvDiff
  have vwa := pair_active b pairs _ _ hv hw _ (label_bounds n cup caps cups v w vw w.isLt) vwDiff
  exact compressed_growth b growth _ hv _ _ uva vwa ⟨uvDiff.1,vwDiff.2⟩
    ((labels_increasing n cup caps u v w uv vw w.isLt).1 cap)

theorem block_capacity_ranks {n} (c : Configuration n)
    (caps : ¬(ActualRanks.colorConfig c.cup true).HasNCap 6 (Finset.range n))
    (cups : ActualRanks.Avoids n c.cup true 8) (junction : NoJunction n c.cup)
    (b : Block) (pairs : pairsOK b=true) (growth : growthOK b=true)
    (noOctagon : ¬HasConvexNGon 8 (Finset.univ.image c.point)) :
    (b.support.toFinset∩Finset.univ.image (fun v : Fin n => (ownerIndex n c.cup caps cups junction v).val)).card≤22 := by
  let index := fun v : Fin n=>(ownerIndex n c.cup caps cups junction v).val
  have inj : Function.Injective index := fun _ _ h=>ownerIndex_injective n c.cup caps cups junction (Fin.ext h)
  change (b.support.toFinset∩Finset.univ.image index).card≤22
  rw [support_count index inj b.support]
  apply BaekGeometry.geometric_capacity22 c (ownerNats index b.support)
  · intro u hu; exact Finset.mem_range.mpr (member_bounded index b.support u hu)
  · apply no_four_cap_of_rank2 c.cup (ownerNats index b.support) (fun u v=>compress b (labels n c.cup u v))
    · intro u _ v _ _; exact compress_bounds b _
    · intro u hu v hv w hw uv vw cap
      have un := member_bounded index b.support u hu
      have vn := member_bounded index b.support v hv
      have wn := member_bounded index b.support w hw
      exact actual_compressed_growth n c.cup caps cups junction b pairs growth
        ⟨u,un⟩ ⟨v,vn⟩ ⟨w,wn⟩
        ((nat_mem_iff index b.support ⟨u,un⟩).mp hu)
        ((nat_mem_iff index b.support ⟨v,vn⟩).mp hv)
        ((nat_mem_iff index b.support ⟨w,wn⟩).mp hw) uv vw cap
  · exact noOctagon

/-- A finite compression check gives the literal missing-state inequality
for actual residual points; the supporting-line transfer is already proved. -/
theorem block_hole_bound {n} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n))
    (b : Block) (pairs : pairsOK b = true) (growth : growthOK b = true)
    (s : Finset (Fin 154)) (hs : b.support.toFinset = s.image Fin.val) :
    s.card - 22 ≤ (s \ c.residualOccupied noCap noOctagon noJunction).card := by
  classical
  have cap := block_capacity_ranks c (fun h => noCap (ListGeometry.hasCap_of_list c h))
    (c.residual_avoids_cup noOctagon) (noJunction_of_lists n c.cup noJunction)
    b pairs growth noOctagon
  change (b.support.toFinset ∩ Finset.univ.image
    (fun v => (c.residualOwner noCap noOctagon noJunction v).val)).card ≤ 22 at cap
  have image_eq : Finset.univ.image (fun v => (c.residualOwner noCap noOctagon noJunction v).val) =
      (c.residualOccupied noCap noOctagon noJunction).image Fin.val := by
    simp [Configuration.residualOccupied, Finset.image_image, Function.comp_def]
  rw [hs, image_eq, ← Finset.image_inter _ _ Fin.val_injective,
    Finset.card_image_of_injective _ Fin.val_injective] at cap
  have count := Finset.card_sdiff_add_card_inter s (c.residualOccupied noCap noOctagon noJunction)
  omega

end ErdosSzekeres.Omission.BlockGeometry
