/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891, ES8ThreeChain.lean.
Code: MIT, copyright (c) 2026 Michael Schroeder; see docs/SCHROEDER-MIT.txt.
Changes: real points as Fin 2 → ℝ, local geometry and namespaces, Lean 4.24.
-/
import ErdosSzekeres.Omission.SlopePartition
import ErdosSzekeres.Omission.CupExtension

namespace ErdosSzekeres.Omission.ThreeChain
open ActualRanks ListGeometry PlanarChains CupExtension

/-- The geometric four-point closure, for either actual orientation. -/
theorem four {n} (c : Configuration n) {a b d e : Nat}
    (ab : a<b) (bd : b<d) (de : d<e) (en : e<n) (k : Bool)
    (h1 : c.cup a b d=k) (h2 : c.cup b d e=k) :
    c.cup a b e=k ∧ c.cup a d e=k := by
  have an : a<n := by omega
  have bn : b<n := by omega
  have dn : d<n := by omega
  cases k with
  | true =>
    have h := positive_four _ _ _ _ (pointAt_order c an bn ab)
      (pointAt_order c bn dn bd) (pointAt_order c dn en de)
      ((cup_sign c a b d an bn dn).mp h1) ((cup_sign c b d e bn dn en).mp h2)
    exact ⟨(cup_sign c a b e an bn en).mpr h.1,(cup_sign c a d e an dn en).mpr h.2⟩
  | false =>
    have h := negative_four _ _ _ _ (pointAt_order c an bn ab)
      (pointAt_order c bn dn bd) (pointAt_order c dn en de)
      ((cap_sign c a b d an bn dn ab bd).mp (by simp [h1]))
      ((cap_sign c b d e bn dn en bd de).mp (by simp [h2]))
    constructor
    · have := (cap_sign c a b e an bn en ab (by omega)).mpr h.1
      simpa using this
    · have := (cap_sign c a d e an dn en (by omega) de).mpr h.2
      simpa using this

theorem left_replace {n} (c : Configuration n) {a b d e : Nat}
    (ab : a<b) (bd : b<d) (de : d<e) (en : e<n)
    (h1 : c.cup a b e=true) (h2 : c.cup b d e=false) : c.cup a b d=true := by
  cases h : c.cup a b d with
  | true => rfl
  | false => have := (four c ab bd de en false h h2).1; simp [h1] at this

theorem right_replace {n} (c : Configuration n) {a b d e : Nat}
    (ab : a<b) (bd : b<d) (de : d<e) (en : e<n)
    (h1 : c.cup a b d=true) (h2 : c.cup a d e=false) : c.cup b d e=false := by
  cases h : c.cup b d e with
  | false => rfl
  | true => have := (four c ab bd de en true h1 h).2; simp [h2] at this

/-- The n=8 three-chain lemma. Outgoing chains may share any interior points;
only their specified endpoint exception is excluded. -/
theorem three_chain {n} (c : Configuration n)
    (x1 x2 x3 x4 x5 s q r3 r4 r5 r6 a b d v u t : Nat)
    (incoming : (colorConfig c.cup true).Cup [x1,x2,x3,x4,x5,s])
    (outcap : (colorConfig c.cup false).Cup [s,q,r3,r4,r5,r6])
    (outcup : (colorConfig c.cup true).Cup [s,a,b,d,v,u,t])
    (sn : s<n) (rn : r6<n) (tn : t<n) (exception : q≠t)
    (noCap : ¬(colorConfig c.cup true).HasNCap 7 (Finset.range n))
    (noOct : ¬HasConvexNGon 8 (Finset.univ.image c.point)) : False := by
  have ci := incoming
  have cq := outcap
  have cp := outcup
  simp only [Config.Cup.cons3,Config.Cup.pair,colorConfig] at ci cq cp
  obtain ⟨x12,h123,x23,h234,x34,h345,x45,h45s,x5s⟩ := ci
  obtain ⟨sq,hsqr,qr3,hqr,r34,hr345,r45,hr456,r56⟩ := cq
  obtain ⟨sa,hsab,ab,habd,bd,hbdv,dv,hdvu,vu,hvut,ut⟩ := cp
  have qn : q<n := by omega
  have un : u<n := by omega
  have vn : v<n := by omega
  have forbid7 (xs : List Nat) (h : (colorConfig c.cup false).Cup xs)
      (len : xs.length=7) (inside : xs.In (Finset.range n)) : False :=
    noCap ⟨xs,⟨(false_cup_iff_cap _ _).mp h,len⟩,inside⟩
  have forbid8 (xs : List Nat) (h : (colorConfig c.cup true).Cup xs)
      (len : xs.length=8) (inside : xs.In (Finset.range n)) : False :=
    noOct (hasNCup_octagon c ⟨xs,⟨h,len⟩,inside⟩)
  have hx5sq : c.cup x5 s q=true := by
    cases h : c.cup x5 s q with
    | true => rfl
    | false =>
      exfalso
      apply forbid7 [x5,s,q,r3,r4,r5,r6]
      · simpa only [Config.Cup.cons3,Config.Cup.pair,colorConfig] using
          And.intro x5s (And.intro h ⟨sq,hsqr,qr3,hqr,r34,hr345,r45,hr456,r56⟩)
      · rfl
      · intro z hz; simp at hz; apply Finset.mem_range.mpr; omega
  have sut : c.cup s u t=true := by
    apply (cup_sign c s u t sn un tn).mpr
    exact cup_list_all c _ (by
      intro z hz; simp at hz; apply Finset.mem_range.mpr; omega) outcup
      s (by simp) u (by simp) t (by simp) (by omega) ut
  rcases lt_or_gt_of_ne exception with qt | tq
  · cases h : c.cup s q t with
    | false => exact noOct (cup7_cap3 c s a b d v u t q outcup sq qt h tn)
    | true =>
      apply forbid8 [x1,x2,x3,x4,x5,s,q,t]
      · simpa only [Config.Cup.cons3,Config.Cup.pair,colorConfig] using
          And.intro x12 (And.intro h123 ⟨x23,h234,x34,h345,x45,h45s,x5s,hx5sq,sq,h,qt⟩)
      · rfl
      · intro z hz; simp at hz; apply Finset.mem_range.mpr; omega
  · cases htq : c.cup u t q with
    | true =>
      apply forbid8 [s,a,b,d,v,u,t,q]
      · simpa only [Config.Cup.cons3,Config.Cup.pair,colorConfig] using
          And.intro sa (And.intro hsab ⟨ab,habd,bd,hbdv,dv,hdvu,vu,hvut,ut,htq,tq⟩)
      · rfl
      · intro z hz; simp at hz; apply Finset.mem_range.mpr; omega
    | false =>
      cases hstq : c.cup s t q with
      | true =>
        have htqr := right_replace c (by omega) tq qr3 (by omega) hstq hsqr
        apply forbid7 [u,t,q,r3,r4,r5,r6]
        · simpa only [Config.Cup.cons3,Config.Cup.pair,colorConfig] using
            And.intro ut (And.intro htq ⟨tq,htqr,qr3,hqr,r34,hr345,r45,hr456,r56⟩)
        · rfl
        · intro z hz; simp at hz; apply Finset.mem_range.mpr; omega
      | false =>
        cases hsuq : c.cup s u q with
        | false =>
          have hx5su := left_replace c x5s (by omega) (by omega) qn hx5sq hsuq
          apply forbid8 [x1,x2,x3,x4,x5,s,u,t]
          · simpa only [Config.Cup.cons3,Config.Cup.pair,colorConfig] using
              And.intro x12 (And.intro h123 ⟨x23,h234,x34,h345,x45,h45s,x5s,hx5su,by omega,sut,ut⟩)
          · rfl
          · intro z hz; simp at hz; apply Finset.mem_range.mpr; omega
        | true =>
          cases hvuq : c.cup v u q with
          | true =>
            have replacement : (colorConfig c.cup true).Cup [s,a,b,d,v,u,q] := by
              simpa only [Config.Cup.cons3,Config.Cup.pair,colorConfig] using
                And.intro sa (And.intro hsab ⟨ab,habd,bd,hbdv,dv,hdvu,vu,hvuq,by omega⟩)
            exact noOct (cup7_cap3 c s a b d v u q t replacement (by omega) tq hstq qn)
          | false =>
            have huqr := right_replace c (by omega) (by omega) qr3 (by omega) hsuq hsqr
            apply forbid7 [v,u,q,r3,r4,r5,r6]
            · simpa only [Config.Cup.cons3,Config.Cup.pair,colorConfig] using
                And.intro vu (And.intro hvuq ⟨by omega,huqr,qr3,hqr,r34,hr345,r45,hr456,r56⟩)
            · rfl
            · intro z hz; simp at hz; apply Finset.mem_range.mpr; omega


end ErdosSzekeres.Omission.ThreeChain
