/-
Adapted from Michael Schroeder, version-1 archive, 19 September 2026,
DOI 10.5281/zenodo.22842891. MIT, copyright (c) 2026 Michael Schroeder.
See docs/SCHROEDER-MIT.txt. Changes: local namespaces and Lean 4.24 APIs.
-/
import ErdosSzekeres.Omission.PlanarChains
import ErdosSzekeres.Basic

namespace ErdosSzekeres.Omission.BoundaryGeometry
def affine (A B C : ℝ) (p : Point) : ℝ := A*p 0+B*p 1+C

theorem affine_mix (A B C a b : ℝ) (x y : Point) (hab : a+b=1) :
    affine A B C (a • x + b • y) = a*affine A B C x + b*affine A B C y := by
  change A*(a*x 0+b*y 0)+B*(a*x 1+b*y 1)+C = a*(A*x 0+B*x 1+C)+b*(A*y 0+B*y 1+C)
  nlinarith [congrArg (fun z : ℝ => z*C) hab]

theorem affine_positive_convex (A B C : ℝ) : Convex ℝ {x : Point | 0 < affine A B C x} := by
  intro x hx y hy a b ha hb hab
  change 0 < affine A B C (a • x + b • y)
  rw [affine_mix A B C a b x y hab]
  change 0 < affine A B C x at hx
  change 0 < affine A B C y at hy
  by_cases hz : a=0
  · subst a
    have he : b=1 := by linarith
    simpa [he] using hy
  · have hp : 0<a := lt_of_le_of_ne ha (Ne.symm hz)
    exact add_pos_of_pos_of_nonneg (mul_pos hp hx) (mul_nonneg hb (le_of_lt hy))

theorem exposed_not_in_hull (S : Set Point) (p : Point) (A B C : ℝ)
    (zero : affine A B C p = 0)
    (positive : ∀ q ∈ S \ {p}, 0 < affine A B C q) :
    p ∉ convexHull ℝ (S \ {p}) := by
  intro hp
  have subset : convexHull ℝ (S \ {p}) ⊆ {q : Point | 0 < affine A B C q} :=
    convexHull_min positive (affine_positive_convex A B C)
  have hx := subset hp
  change 0 < affine A B C p at hx
  rw [zero] at hx
  exact (lt_irrefl 0) hx

/-- Two supporting oriented edges expose their shared vertex. -/
theorem supporting_edges_expose (S : Set Point) (u v w : Point)
    (support : ∀ p ∈ S \ {v}, 0 < orient u v p + orient v w p) :
    v ∉ convexHull ℝ (S \ {v}) := by
  let A := u 1-w 1
  let B := w 0-u 0
  let C := (v 1-u 1)*u 0-(v 0-u 0)*u 1+(w 1-v 1)*v 0-(w 0-v 0)*v 1
  have eq : ∀ p : Point, affine A B C p = orient u v p + orient v w p := by
    intro p; dsimp [affine, orient, A, B, C]; ring
  apply exposed_not_in_hull S v A B C
  · rw [eq]; dsimp [orient]; ring
  · intro p hp; rw [eq]; exact support p hp

/-- A genuinely geometric lower arc, including both endpoints. -/
structure CupArc (k : Nat) where
  point : Fin (k+2) → Point
  xOrder : StrictMono (fun i => point i 0)
  positive : ∀ i j l, i<j → j<l → 0<orient (point i) (point j) (point l)

def first {k} (p : CupArc k) := p.point 0
def last {k} (p : CupArc k) := p.point ⟨k+1, by omega⟩

theorem chord_identity (s t a b v : Point) :
    (t 0-s 0)*orient a b v = (t 0-v 0)*orient a b s +
      (v 0-s 0)*orient a b t + (b 0-a 0)*orient s t v := by
  unfold orient; ring

def reflect (p : Point) : Point := ![p 0,-p 1]
@[simp] theorem reflect_reflect (p : Point) : reflect (reflect p)=p := by ext i; fin_cases i <;> simp [reflect]
@[simp] theorem orient_reflect (p q r : Point) :
    orient (reflect p) (reflect q) (reflect r) = -orient p q r := by
  simp [orient, reflect]; ring

theorem edge_positive {k} (p : CupArc k) (i : Fin (k+1)) (j : Fin (k+2))
    (left : j.val≠i.val) (right : j.val≠i.val+1) :
    0<orient (p.point ⟨i.val,by omega⟩) (p.point ⟨i.val+1,by omega⟩) (p.point j) := by
  by_cases h : j.val < i.val
  · have hp := p.positive j ⟨i.val,by omega⟩ ⟨i.val+1,by omega⟩ h (by simp)
    rwa [← orient_cycle] at hp
  · exact p.positive _ _ j (by change i.val < i.val+1; omega) (by change i.val+1 < j.val; omega)

theorem edge_nonnegative {k} (p : CupArc k) (i : Fin (k+1)) (j : Fin (k+2)) :
    0≤orient (p.point ⟨i.val,by omega⟩) (p.point ⟨i.val+1,by omega⟩) (p.point j) := by
  by_cases h : j.val=i.val
  · have he : j=⟨i.val,by omega⟩ := Fin.ext h
    rw [he]; unfold orient; nlinarith
  · by_cases h' : j.val=i.val+1
    · have he : j=⟨i.val+1,by omega⟩ := Fin.ext h'
      rw [he]; unfold orient; nlinarith
    · exact le_of_lt (edge_positive p i j h h')

theorem point_x_bounds {k} (p : CupArc k) (j : Fin (k+2)) :
    (first p) 0≤(p.point j) 0 ∧ (p.point j) 0≤(last p) 0 := by
  exact ⟨p.xOrder.monotone (by simp),p.xOrder.monotone (by change j.val≤k+1; omega)⟩

theorem chord_nonpositive {k} (p : CupArc k) (j : Fin (k+2)) :
    orient (first p) (last p) (p.point j) ≤ 0 := by
  by_cases h : j.val=0
  · have he : j=0 := Fin.ext h
    rw [he]; simp [first,orient]
  · by_cases h' : j.val=k+1
    · have he : j=⟨k+1,by omega⟩ := Fin.ext h'
      rw [he]; unfold last orient; nlinarith
    · have hp := p.positive 0 j ⟨k+1,by omega⟩ (by change 0<j.val; omega) (by change j.val<k+1; omega)
      have eq : orient (first p) (last p) (p.point j) = -orient (first p) (p.point j) (last p) := by
        unfold orient; ring
      rw [eq]; exact le_of_lt (neg_neg_of_pos hp)

theorem chord_negative {k} (p : CupArc k) (j : Fin (k+2))
    (hl : 0<j.val) (hr : j.val<k+1) :
    orient (first p) (last p) (p.point j)<0 := by
  have hp := p.positive 0 j ⟨k+1,by omega⟩ hl hr
  have eq : orient (first p) (last p) (p.point j) = -orient (first p) (p.point j) (last p) := by
    unfold orient; ring
  rw [eq]; exact neg_neg_of_pos hp

/-- A cap is represented as the reflection of a cup. The actual upper points
are `reflect (q.point i)`, not the reflected coordinates themselves. -/
structure Boundary (k l : Nat) where
  lower : CupArc k
  upperReflected : CupArc l
  first_eq : first lower = reflect (first upperReflected)
  last_eq : last lower = reflect (last upperReflected)

def Boundary.points {k l} (b : Boundary k l) : Set Point :=
  Set.range b.lower.point ∪ Set.range (fun j => reflect (b.upperReflected.point j))

theorem cross_edge_positive {k l} (b : Boundary k l) (i : Fin (k+1)) (j : Fin (l+2))
    (hl : 0<j.val) (hr : j.val<l+1) :
    0<orient (b.lower.point ⟨i.val,by omega⟩) (b.lower.point ⟨i.val+1,by omega⟩)
      (reflect (b.upperReflected.point j)) := by
  let p := b.lower
  let q := b.upperReflected
  let v := reflect (q.point j)
  have bounds : (first p) 0≤v 0 ∧ v 0≤(last p) 0 := by
    simpa [p,q,v,b.first_eq,b.last_eq,reflect] using point_x_bounds q j
  have chord : 0<orient (first p) (last p) v := by
    rw [show first p=reflect (first q) from b.first_eq,show last p=reflect (last q) from b.last_eq]
    simpa [v] using neg_pos.mpr (chord_negative q j hl hr)
  have e1 := edge_nonnegative p i 0
  have e2 := edge_nonnegative p i ⟨k+1,by omega⟩
  have ab : 0<(p.point ⟨i.val+1,by omega⟩) 0-(p.point ⟨i.val,by omega⟩) 0 :=
    sub_pos.mpr (p.xOrder (by change i.val < i.val+1; omega))
  have st : 0<(last p) 0-(first p) 0 := sub_pos.mpr (p.xOrder (by change 0<k+1; omega))
  have id := chord_identity (first p) (last p) (p.point ⟨i.val,by omega⟩)
    (p.point ⟨i.val+1,by omega⟩) v
  have t1 := mul_nonneg (sub_nonneg.mpr bounds.2) e1
  have t2 := mul_nonneg (sub_nonneg.mpr bounds.1) e2
  have t3 := mul_pos ab chord
  apply (mul_pos_iff_of_pos_left st).mp
  change 0<((last p) 0-(first p) 0)*orient _ _ v
  rw [id]
  exact add_pos_of_nonneg_of_pos (add_nonneg t1 t2) t3

/-- Each lower edge supports the entire actual boundary, strictly away from
its two endpoints. This includes upper points whose x positions interleave. -/
theorem lower_edge_support {k l} (b : Boundary k l) (i : Fin (k+1)) (v : Point)
    (hv : v∈b.points) :
    0≤orient (b.lower.point ⟨i.val,by omega⟩) (b.lower.point ⟨i.val+1,by omega⟩) v ∧
    (v≠b.lower.point ⟨i.val,by omega⟩ → v≠b.lower.point ⟨i.val+1,by omega⟩ →
      0<orient (b.lower.point ⟨i.val,by omega⟩) (b.lower.point ⟨i.val+1,by omega⟩) v) := by
  have own : ∀ j : Fin (k+2), _ := fun j => edge_nonnegative b.lower i j
  rcases hv with ⟨j,rfl⟩ | ⟨j,rfl⟩
  · refine ⟨edge_nonnegative b.lower i j,?_⟩
    intro h1 h2
    apply edge_positive b.lower i j
    · intro he; exact h1 (congrArg b.lower.point (Fin.ext he))
    · intro he; exact h2 (congrArg b.lower.point (Fin.ext he))
  · dsimp only
    by_cases h : j.val=0
    · have he : j=0 := Fin.ext h
      rw [he,show reflect (b.upperReflected.point 0)=b.lower.point 0 from b.first_eq.symm]
      refine ⟨edge_nonnegative b.lower i 0,?_⟩
      intro h1 h2
      apply edge_positive b.lower i 0
      · intro he; exact h1 (congrArg b.lower.point (Fin.ext he))
      · intro he; exact h2 (congrArg b.lower.point (Fin.ext he))
    · by_cases h' : j.val=l+1
      · have he : j=⟨l+1,by omega⟩ := Fin.ext h'
        rw [he,show reflect (b.upperReflected.point ⟨l+1,by omega⟩)=b.lower.point ⟨k+1,by omega⟩ from b.last_eq.symm]
        refine ⟨edge_nonnegative b.lower i ⟨k+1,by omega⟩,?_⟩
        intro h1 h2
        apply edge_positive b.lower i ⟨k+1,by omega⟩
        · intro he; exact h1 (congrArg b.lower.point (Fin.ext he))
        · intro he; exact h2 (congrArg b.lower.point (Fin.ext he))
      · have hp := cross_edge_positive b i j (by omega) (by omega)
        exact ⟨le_of_lt hp,fun _ _=>hp⟩

def Boundary.flip {k l} (b : Boundary k l) : Boundary l k where
  lower := b.upperReflected
  upperReflected := b.lower
  first_eq := by rw [b.first_eq,reflect_reflect]
  last_eq := by rw [b.last_eq,reflect_reflect]

theorem reflect_mem_flip {k l} (b : Boundary k l) {v : Point} (hv : v∈b.points) :
    reflect v∈b.flip.points := by
  rcases hv with ⟨i,rfl⟩ | ⟨j,rfl⟩
  · exact Or.inr ⟨i,rfl⟩
  · exact Or.inl ⟨j,reflect_reflect _ |>.symm⟩

theorem upper_edge_support {k l} (b : Boundary k l) (i : Fin (l+1)) (v : Point)
    (hv : v∈b.points) :
    0≤orient (reflect (b.upperReflected.point ⟨i.val+1,by omega⟩))
      (reflect (b.upperReflected.point ⟨i.val,by omega⟩)) v ∧
    (v≠reflect (b.upperReflected.point ⟨i.val+1,by omega⟩) →
     v≠reflect (b.upperReflected.point ⟨i.val,by omega⟩) →
      0<orient (reflect (b.upperReflected.point ⟨i.val+1,by omega⟩))
        (reflect (b.upperReflected.point ⟨i.val,by omega⟩)) v) := by
  have h := lower_edge_support b.flip i (reflect v) (reflect_mem_flip b hv)
  have eq : orient (reflect (b.upperReflected.point ⟨i.val+1,by omega⟩))
      (reflect (b.upperReflected.point ⟨i.val,by omega⟩)) v =
      orient (b.upperReflected.point ⟨i.val,by omega⟩)
        (b.upperReflected.point ⟨i.val+1,by omega⟩) (reflect v) := by
    simp [orient, reflect]; ring
  rw [eq]
  refine ⟨h.1,?_⟩
  intro h1 h2
  apply h.2
  · intro he; apply h2; simpa [Boundary.flip] using congrArg reflect he
  · intro he; apply h1; simpa [Boundary.flip] using congrArg reflect he

theorem two_edges_expose (S : Set Point) (u v w : Point) (uw : u≠w)
    (left : ∀ p∈S, 0≤orient u v p ∧ (p≠u → p≠v → 0<orient u v p))
    (right : ∀ p∈S, 0≤orient v w p ∧ (p≠v → p≠w → 0<orient v w p)) :
    v∉convexHull ℝ (S\{v}) := by
  apply supporting_edges_expose S u v w
  intro p hp
  have l := left p hp.1
  have r := right p hp.1
  have pv : p≠v := hp.2
  by_cases pu : p=u
  · have pw : p≠w := by simpa [pu] using uw
    exact add_pos_of_nonneg_of_pos l.1 (r.2 pv pw)
  · exact add_pos_of_pos_of_nonneg (l.2 pu pv) r.1

theorem lower_interior_exposed {k l} (b : Boundary k l) (j : Fin (k+2))
    (hl : 0<j.val) (hr : j.val<k+1) :
    b.lower.point j∉convexHull ℝ (b.points\{b.lower.point j}) := by
  let prev : Fin (k+2) := ⟨j.val-1,by omega⟩
  let next : Fin (k+2) := ⟨j.val+1,by omega⟩
  apply two_edges_expose b.points (b.lower.point prev) (b.lower.point j) (b.lower.point next)
  · intro he
    have hx := b.lower.xOrder (show prev<next by change j.val-1<j.val+1; omega)
    dsimp only at hx
    rw [he] at hx; exact (lt_irrefl _ hx)
  · intro v hv
    have h := lower_edge_support b ⟨j.val-1,by omega⟩ v hv
    have eq : (⟨j.val-1+1,by omega⟩ : Fin (k+2))=j := by apply Fin.ext; change j.val-1+1=j.val; omega
    simpa only [eq] using h
  · exact fun v hv => lower_edge_support b ⟨j.val,by omega⟩ v hv

theorem upper_interior_exposed {k l} (b : Boundary k l) (j : Fin (l+2))
    (hl : 0<j.val) (hr : j.val<l+1) :
    reflect (b.upperReflected.point j)∉convexHull ℝ (b.points\{reflect (b.upperReflected.point j)}) := by
  let prev : Fin (l+2) := ⟨j.val-1,by omega⟩
  let next : Fin (l+2) := ⟨j.val+1,by omega⟩
  apply two_edges_expose b.points (reflect (b.upperReflected.point next))
    (reflect (b.upperReflected.point j)) (reflect (b.upperReflected.point prev))
  · intro he
    have hx := b.upperReflected.xOrder (show prev<next by change j.val-1<j.val+1; omega)
    have he' := congrArg (fun p : Point => p 0) he
    change (b.upperReflected.point next) 0=(b.upperReflected.point prev) 0 at he'
    linarith
  · exact fun v hv => upper_edge_support b ⟨j.val,by omega⟩ v hv
  · intro v hv
    have h := upper_edge_support b ⟨j.val-1,by omega⟩ v hv
    have eq : (⟨j.val-1+1,by omega⟩ : Fin (l+2))=j := by apply Fin.ext; change j.val-1+1=j.val; omega
    simpa only [eq] using h

theorem first_x_strict {k} (p : CupArc k) (j : Fin (k+2)) (h : p.point j≠first p) :
    (first p) 0<(p.point j) 0 := by
  apply p.xOrder
  change 0<j.val
  by_contra hn
  have he : j=0 := by apply Fin.ext; change j.val=0; omega
  exact h (congrArg p.point he)

theorem last_x_strict {k} (p : CupArc k) (j : Fin (k+2)) (h : p.point j≠last p) :
    (p.point j) 0<(last p) 0 := by
  apply p.xOrder
  change j.val<k+1
  by_contra hn
  have he : j=⟨k+1,by omega⟩ := by apply Fin.ext; change j.val=k+1; omega
  exact h (congrArg p.point he)

theorem boundary_first_exposed {k l} (b : Boundary k l) :
    first b.lower∉convexHull ℝ (b.points\{first b.lower}) := by
  apply exposed_not_in_hull b.points (first b.lower) 1 0 (-(first b.lower) 0)
  · simp [affine]
  · intro v hv
    have h : (first b.lower) 0<v 0 := by
      rcases hv.1 with ⟨j,rfl⟩ | ⟨j,rfl⟩
      · exact first_x_strict b.lower j hv.2
      · have ne : b.upperReflected.point j≠first b.upperReflected := by
          intro he; apply hv.2; change reflect (b.upperReflected.point j)=first b.lower; rw [he]; exact b.first_eq.symm
        simpa [b.first_eq,reflect] using first_x_strict b.upperReflected j ne
    change 0<1*v 0+0*v 1+(-(first b.lower) 0)
    linarith

theorem boundary_last_exposed {k l} (b : Boundary k l) :
    last b.lower∉convexHull ℝ (b.points\{last b.lower}) := by
  apply exposed_not_in_hull b.points (last b.lower) (-1) 0 ((last b.lower) 0)
  · simp [affine]
  · intro v hv
    have h : v 0<(last b.lower) 0 := by
      rcases hv.1 with ⟨j,rfl⟩ | ⟨j,rfl⟩
      · exact last_x_strict b.lower j hv.2
      · have ne : b.upperReflected.point j≠last b.upperReflected := by
          intro he; apply hv.2; change reflect (b.upperReflected.point j)=last b.lower; rw [he]; exact b.last_eq.symm
        simpa [b.last_eq,reflect] using last_x_strict b.upperReflected j ne
    change 0<(-1)*v 0+0*v 1+(last b.lower) 0
    linarith

/-- Every real cup/cap boundary with common endpoints is in convex position.
No disjointness premise is inserted: the geometry itself separates interiors. -/
theorem boundary_convex_position {k l} (b : Boundary k l) : ∀ v ∈ b.points, v ∉ convexHull ℝ (b.points \ {v}) := by
  intro v hv
  rcases hv with ⟨j,rfl⟩ | ⟨j,rfl⟩
  · by_cases h : j.val=0
    · have he : j=0 := Fin.ext h
      rw [he]; exact boundary_first_exposed b
    · by_cases h' : j.val=k+1
      · have he : j=⟨k+1,by omega⟩ := Fin.ext h'
        rw [he]; exact boundary_last_exposed b
      · exact lower_interior_exposed b j (by omega) (by omega)
  · dsimp only
    by_cases h : j.val=0
    · have he : j=0 := Fin.ext h
      rw [he,show reflect (b.upperReflected.point 0)=first b.lower from b.first_eq.symm]
      exact boundary_first_exposed b
    · by_cases h' : j.val=l+1
      · have he : j=⟨l+1,by omega⟩ := Fin.ext h'
        rw [he,show reflect (b.upperReflected.point ⟨l+1,by omega⟩)=last b.lower from b.last_eq.symm]
        exact boundary_last_exposed b
      · exact upper_interior_exposed b j (by omega) (by omega)

theorem shared_only_endpoints {k l} (b : Boundary k l) (i : Fin (k+2)) (j : Fin (l+2))
    (eq : b.lower.point i=reflect (b.upperReflected.point j)) : i.val=0 ∨ i.val=k+1 := by
  by_contra h
  have hi : 0 < i.val ∧ i.val < k+1 := by omega
  have neg := chord_negative b.lower i hi.1 hi.2
  have nn := chord_nonpositive b.upperReflected j
  have re : orient (first b.lower) (last b.lower) (b.lower.point i) =
      -orient (first b.upperReflected) (last b.upperReflected) (b.upperReflected.point j) := by
    rw [eq,b.first_eq,b.last_eq,orient_reflect]
  rw [re] at neg
  linarith

noncomputable def Boundary.finite {k l} (b : Boundary k l) : Finset Point := by
  classical
  exact Finset.univ.image b.lower.point ∪ Finset.univ.image (fun j => reflect (b.upperReflected.point j))

theorem Boundary.finite_coe {k l} (b : Boundary k l) : (↑b.finite : Set Point)=b.points := by
  classical
  ext v
  simp [Boundary.finite,Boundary.points]

theorem Boundary.card {k l} (b : Boundary k l) : b.finite.card=k+l+2 := by
  classical
  let lower := Finset.univ.image b.lower.point
  let upper := Finset.univ.image (fun j => reflect (b.upperReflected.point j))
  have lower_inj : Function.Injective b.lower.point := by
    intro i j he; exact b.lower.xOrder.injective (congrArg (fun p : Point => p 0) he)
  have upper_inj : Function.Injective (fun j => reflect (b.upperReflected.point j)) := by
    intro i j he
    apply b.upperReflected.xOrder.injective
    simpa [reflect] using congrArg (fun p : Point => p 0) he
  have lc : lower.card=k+2 := by simp [lower,Finset.card_image_of_injective _ lower_inj]
  have uc : upper.card=l+2 := by simp [upper,Finset.card_image_of_injective _ upper_inj]
  have inter : lower∩upper={first b.lower,last b.lower} := by
    ext v
    constructor
    · intro hv
      obtain ⟨i,_,hi⟩ := Finset.mem_image.mp (Finset.mem_inter.mp hv).1
      obtain ⟨j,_,hj⟩ := Finset.mem_image.mp (Finset.mem_inter.mp hv).2
      have ie := shared_only_endpoints b i j (hi.trans hj.symm)
      rcases ie with he | he
      · have ie : i=0 := Fin.ext he
        have ve : v=first b.lower := by rw [←hi,ie]; rfl
        simp [ve]
      · have ie : i=⟨k+1,by omega⟩ := Fin.ext he
        have ve : v=last b.lower := by rw [←hi,ie]; rfl
        simp [ve]
    · intro hv
      rcases Finset.mem_insert.mp hv with rfl | hv
      · exact Finset.mem_inter.mpr ⟨Finset.mem_image.mpr ⟨0,by simp,rfl⟩,
          Finset.mem_image.mpr ⟨0,by simp,b.first_eq.symm⟩⟩
      · have he : v=last b.lower := Finset.mem_singleton.mp hv
        subst v
        exact Finset.mem_inter.mpr ⟨Finset.mem_image.mpr ⟨⟨k+1,by omega⟩,by simp,rfl⟩,
          Finset.mem_image.mpr ⟨⟨l+1,by omega⟩,by simp,b.last_eq.symm⟩⟩
  have distinct : first b.lower≠last b.lower := by
    intro he
    have hx := b.lower.xOrder (show (0 : Fin (k+2))<⟨k+1,by omega⟩ by change 0<k+1; omega)
    change (first b.lower) 0<(last b.lower) 0 at hx
    rw [he] at hx; exact lt_irrefl _ hx
  have ic : (lower∩upper).card=2 := by rw [inter]; simp [distinct]
  have total := Finset.card_union_add_card_inter lower upper
  change (lower∪upper).card=k+l+2
  omega

theorem boundary_polygon {k l} (b : Boundary k l)
    (S : Finset Point) (inside : b.points ⊆ (S : Set Point)) :
    HasConvexNGon (k+l+2) S := by
  refine ⟨b.finite, ?_, b.card, ?_⟩
  · intro p hp
    exact inside (by rwa [← b.finite_coe])
  · apply (convexPosition_iff b.finite).mpr
    rw [b.finite_coe]
    exact boundary_convex_position b

end ErdosSzekeres.Omission.BoundaryGeometry
