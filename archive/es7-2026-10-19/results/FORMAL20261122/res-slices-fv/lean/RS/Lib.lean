/-
res-slices-fv (22 November 2026): generic lemmas for the slice catalogs.

A slice catalog is the trie of `CompactChecker.fcat2650` (the 2,650 base rows of the residual system, olean pinned by
the verified ES(8) ≤ 311 assembly) with the slice's extra rows added at 2650 (F, T), 2651 (Lo, B − T) and 2652 + j
(unit rows), Res118's numbering. `sliceCatalog_of` reduces `Res118.SliceCatalog` to kernel-checkable Bool/list facts:
* `baseAgree cat`: on every base index r < 2650 the new trie has fcat2650's support and demand; with
  `Bridge311Res.res_support` / `res_demand` (imported, not re-proved) this gives the base-row identities;
* the two capacity rows as literal lists (`Res118.fIndices`, `Res118.loIndices`, pinned to `F`, `Lo` by `F_eq`,
  `Lo_eq`) and demands;
* the unit rows as one list equality, and their demands 1.
-/
import CompactChecker.Path
import CompactChecker.Bridge311Res
import Res118.Adapter

open scoped BigOperators
open ErdosSzekeres.OmissionCertificates CompactChecker OmissionResidual32Bridge2650

namespace RS

theorem wf_node {n b : ℕ} {l r : FCat} :
    (FCat.node l r).wf n b = true ↔ l.wf n b = true ∧ r.wf n b = true := by
  simp [FCat.wf]

/-- The new trie has fcat2650's support and demand at every base index. -/
noncomputable def baseAgree (cat : FCat) : Bool :=
  (List.range 2650).all fun r =>
    decide ((cat.get r).1 = (fcat2650.get r).1) && decide ((cat.get r).2.1 = (fcat2650.get r).2.1)

theorem base_of_agree {cat : FCat} (h : baseAgree cat = true) (r : Fin 2650) :
    (cat.get r.val).1 = (fcat2650.get r.val).1 ∧ (cat.get r.val).2.1 = (fcat2650.get r.val).2.1 := by
  have := List.all_eq_true.mp h r.val (List.mem_range.mpr r.isLt)
  simpa [Bool.and_eq_true, decide_eq_true_eq] using this

theorem fsupp_of_list {cat : FCat} {k : ℕ} {s : List ℕ} {S : Finset (Fin 154)}
    (hl : (cat.get k).1 = s) (hS : ∀ i : Fin 154, i ∈ S ↔ i.val ∈ s) : fsupp cat 154 k = S := by
  ext i
  simp only [fsupp, Finset.mem_filter, Finset.mem_univ, true_and, hl, hS]

/-- `Res118.SliceCatalog` from kernel-checkable facts. -/
theorem sliceCatalog_of {cat : FCat} {rows : List (List ℕ)} {B T : ℕ}
    (hbase : baseAgree cat = true)
    (hF : (cat.get 2650).1 = Res118.fIndices) (hFd : cat.dem 2650 = T)
    (hL : (cat.get 2651).1 = Res118.loIndices) (hLd : cat.dem 2651 = B - T)
    (hU : (List.range rows.length).map (fun j => (cat.get (2652 + j)).1) = rows)
    (hUd : (List.range rows.length).all (fun j => decide (cat.dem (2652 + j) = 1)) = true) :
    Res118.SliceCatalog cat rows B T where
  base_supp r := by
    have e : fsupp cat 154 r.val = fsupp fcat2650 154 r.val := by
      unfold fsupp
      rw [(base_of_agree hbase r).1]
    rw [e]
    exact Bridge311Res.res_support r
  base_dem r := by
    show (cat.get r.val).2.1 = _
    rw [(base_of_agree hbase r).2]
    exact Bridge311Res.res_demand r
  f_supp := fsupp_of_list hF Res118.F_eq
  f_dem := hFd
  lo_supp := fsupp_of_list hL Res118.Lo_eq
  lo_dem := hLd
  unit_supp j hj := by
    have h := congrArg (fun l => l[j]?) hU
    simp only [List.getElem?_map, List.getElem?_range hj, Option.map_some] at h
    rw [List.getElem?_eq_getElem hj] at h
    exact Option.some.inj h
  unit_dem j hj := by
    have := List.all_eq_true.mp hUd j (List.mem_range.mpr hj)
    simpa using this

end RS

#print axioms RS.base_of_agree
#print axioms RS.sliceCatalog_of
