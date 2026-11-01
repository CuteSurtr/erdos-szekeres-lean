/-! Size bookkeeping for the assembled symmetric theorem (finding A1-F1), core Lean only.
  n = size of the symmetric set, k = number of non-central orbits (or off-axis pairs),
  e = 1 iff the rotation centre is a point of the set, b = number of points on the mirror axis. -/

-- half-turn (the finding's one line): centre excluded geometrically, so n = 2k; n >= 33 gives 17 pairs
theorem halfturn_pairs (n k : Nat) (h : n = 2 * k) (h33 : 33 ≤ n) : 17 ≤ k ∧ 34 ≤ n := by omega

-- threefold: n = 3k + e, e <= 1; n >= 33 gives 11 whole orbits
theorem threefold_orbits (n k e : Nat) (he : e ≤ 1) (h : n = 3 * k + e) (h33 : 33 ≤ n) : 11 ≤ k := by omega

-- fivefold: n = 5k + e, e <= 1; n >= 33 forces n >= 35 (sizes 33 and 34 impossible)
theorem fivefold_size (n k e : Nat) (he : e ≤ 1) (h : n = 5 * k + e) (h33 : 33 ≤ n) : 35 ≤ n := by omega

-- mirror, no axis point: n = 2k; 17 pairs
theorem mirror_b0 (n k : Nat) (h : n = 2 * k) (h33 : 33 ≤ n) : 17 ≤ k := by omega

-- mirror, one or two axis points: n = 2k + b; 16 pairs (plus one axis point)
theorem mirror_b12 (n k b : Nat) (hb1 : 1 ≤ b) (hb2 : b ≤ 2) (h : n = 2 * k + b) (h33 : 33 ≤ n) : 16 ≤ k := by omega

-- fourfold sets are half-turn sets: n = 4k (centre excluded), so 2k antipodal pairs, at least 17
theorem fourfold_via_halfturn (n k : Nat) (h : n = 4 * k) (h33 : 33 ≤ n) : 17 ≤ 2 * k := by omega

-- prime order p >= 7: at least one non-central orbit when n >= 33 and e <= 1
theorem big_order_orbit (n k e p : Nat) (hp : 7 ≤ p) (he : e ≤ 1) (h : n = p * k + e) (h33 : 33 ≤ n) : 1 ≤ k := by
  cases k with
  | zero => simp at h; omega
  | succ k => omega

-- control: the half-turn line is false below 33 (32 points = 16 pairs; the central 32-point example exists)
example : ¬ (∀ n k : Nat, n = 2 * k → 32 ≤ n → 17 ≤ k) := by
  intro h; have := h 32 16 rfl (by decide); omega

#print axioms halfturn_pairs
#print axioms threefold_orbits
#print axioms fivefold_size
#print axioms mirror_b0
#print axioms mirror_b12
#print axioms fourfold_via_halfturn
#print axioms big_order_orbit
