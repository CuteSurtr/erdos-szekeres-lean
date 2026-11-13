/-
A1 audit: the size arithmetic of the symmetric ES(7) reduction, for ALL sizes n (core Lean 4, no Mathlib).

Modelling (audited by hand in the report, not formalised here):
  rotation of order s about c: n = s*k + e, k = number of non-centre orbits, e = 1 iff c ∈ S, e ≤ 1,
  and e = 0 when s is even (c would be collinear with p and -p);
  reflection: n = 2*k + b, k = number of mirror pairs, b = number of axis points, b ≤ 2.
Deleting whole orbits / the centre / axis points keeps the symmetry and general position.
-/

namespace A1

/-! ## Reduction (Corollary 3 + the central case), every n ≥ 33 -/

/-- threefold: at least 11 non-central orbits, i.e. a 33-point C3 subset without centre (T_C3). -/
theorem c3_reduce (k e : Nat) (he : e ≤ 1) (hn : 33 ≤ 3 * k + e) : 11 ≤ k := by omega

/-- fivefold: sizes 33 and 34 are impossible, so n ≥ 35 (T_C5 applies directly). -/
theorem c5_reduce (k e : Nat) (he : e ≤ 1) (hn : 33 ≤ 5 * k + e) : 35 ≤ 5 * k + e ∧ 7 ≤ k := by omega

/-- fourfold (no centre): n ≥ 36, at least 8 C4-orbits (T_C4) and at least 17 antipodal pairs (T_C2). -/
theorem c4_reduce (k : Nat) (hn : 33 ≤ 4 * k) : 36 ≤ 4 * k ∧ 8 ≤ k ∧ 17 ≤ 2 * k := by omega

/-- sixfold (no centre): at least 11 C3-orbits (T_C3) and at least 17 antipodal pairs (T_C2). -/
theorem c6_reduce (k : Nat) (hn : 33 ≤ 6 * k) : 11 ≤ 2 * k ∧ 17 ≤ 3 * k := by omega

/-- half-turn only (no centre): n even, n ≥ 34, at least 17 pairs (T_C2). -/
theorem c2_reduce (k : Nat) (hn : 33 ≤ 2 * k) : 34 ≤ 2 * k ∧ 17 ≤ k := by omega

/-- mirror, no axis point: n even, n ≥ 34, at least 17 pairs (T_M34). -/
theorem mirror_reduce_b0 (k : Nat) (hn : 33 ≤ 2 * k) : 17 ≤ k := by omega

/-- mirror, one or two axis points: at least 16 pairs, so 16 pairs + 1 axis point (T_M33). -/
theorem mirror_reduce_b12 (k b : Nat) (hb1 : 1 ≤ b) (hb2 : b ≤ 2) (hn : 33 ≤ 2 * k + b) : 16 ≤ k := by omega

/-- general even order s = 2t, no centre: at least 17 antipodal pairs (T_C2). -/
theorem even_order_reduce (t k : Nat) (hn : 33 ≤ 2 * t * k) : 17 ≤ t * k := by
  have : 2 * t * k = 2 * (t * k) := by rw [Nat.mul_assoc]
  omega

/-- order divisible by 3 (s = 3t), centre flag e: at least 11 C3-orbits (T_C3). -/
theorem mult3_order_reduce (t k e : Nat) (he : e ≤ 1) (hn : 33 ≤ 3 * t * k + e) : 11 ≤ t * k := by
  have : 3 * t * k = 3 * (t * k) := by rw [Nat.mul_assoc]
  omega

/-- order divisible by 5 (s = 5t): at least 35 points as a C5-set (T_C5). -/
theorem mult5_order_reduce (t k e : Nat) (he : e ≤ 1) (hn : 33 ≤ 5 * t * k + e) : 35 ≤ 5 * (t * k) + e := by
  have : 5 * t * k = 5 * (t * k) := by rw [Nat.mul_assoc]
  omega

/-- prime-order case split: every s ≥ 2 has 2, 3 or 5 as a divisor, or is ≥ 7. -/
theorem order_split (s : Nat) (hs : 2 ≤ s) : s % 2 = 0 ∨ s % 3 = 0 ∨ s % 5 = 0 ∨ 7 ≤ s := by
  rcases Nat.lt_or_ge s 7 with h | h
  · have hcases : s = 2 ∨ s = 3 ∨ s = 4 ∨ s = 5 ∨ s = 6 := by omega
    rcases hcases with rfl | rfl | rfl | rfl | rfl <;> decide
  · exact Or.inr (Or.inr (Or.inr h))

/-! ## Upper bounds of the table, given the case theorems -/

/-- C3: if not excluded (k ≤ 10), then n ≤ 31; also 32 is not a C3 size. -/
theorem table_c3 (k e : Nat) (he : e ≤ 1) (hk : k ≤ 10) : 3 * k + e ≤ 31 := by omega
theorem c3_no32 (k e : Nat) (he : e ≤ 1) : 3 * k + e ≠ 32 := by omega

/-- C5: if not excluded (n < 35), then n ≤ 31; 32, 33, 34 are not C5 sizes. -/
theorem table_c5 (k e : Nat) (he : e ≤ 1) (hn : 5 * k + e < 35) : 5 * k + e ≤ 31 := by omega
theorem c5_gap (k e : Nat) (he : e ≤ 1) : 5 * k + e ≠ 32 ∧ 5 * k + e ≠ 33 ∧ 5 * k + e ≠ 34 := by omega

/-- C4: if not excluded by T_C4 (k ≤ 7), n ≤ 28; with only T_C2 (2k ≤ 16), n ≤ 32. -/
theorem table_c4 (k : Nat) (hk : k ≤ 7) : 4 * k ≤ 28 := by omega
theorem table_c4_only_c2 (k : Nat) (hk : 2 * k ≤ 16) : 4 * k ≤ 32 := by omega

/-- C6: if not excluded by T_C3 (2k ≤ 10), n ≤ 30. -/
theorem table_c6 (k : Nat) (hk : 2 * k ≤ 10) : 6 * k ≤ 30 := by omega

/-- C2: if not excluded by T_C2 (k ≤ 16), n ≤ 32. -/
theorem table_c2 (k : Nat) (hk : k ≤ 16) : 2 * k ≤ 32 := by omega

/-- mirror: if excluded neither by T_M34 nor by T_M33, then n ≤ 32. -/
theorem table_mirror (k b : Nat) (hb : b ≤ 2) (h34 : b = 0 → k ≤ 16) (h33 : 1 ≤ b → k ≤ 15) :
    2 * k + b ≤ 32 := by omega

end A1

#print axioms A1.c3_reduce
#print axioms A1.c5_reduce
#print axioms A1.c4_reduce
#print axioms A1.c6_reduce
#print axioms A1.c2_reduce
#print axioms A1.mirror_reduce_b0
#print axioms A1.mirror_reduce_b12
#print axioms A1.even_order_reduce
#print axioms A1.mult3_order_reduce
#print axioms A1.mult5_order_reduce
#print axioms A1.order_split
#print axioms A1.table_c3
#print axioms A1.c3_no32
#print axioms A1.table_c5
#print axioms A1.c5_gap
#print axioms A1.table_c4
#print axioms A1.table_c4_only_c2
#print axioms A1.table_c6
#print axioms A1.table_c2
#print axioms A1.table_mirror
