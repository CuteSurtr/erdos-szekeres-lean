# VERIFY_D1_LR7M16_SPLIT: verdict on claim d1-lr7m16-split (verifier VB, 15 November 2026, 21:14-21:16 KST)

**Verdict: CONFIRMED.** The reduction is correct (PROVED; VB checked every case), the two base encoders are sound in the
direction the reduction needs (VB read `lr_compact.py` line by line; `root_compact.py` in VERIFY_D1_C1SIX.md §3), and the
four CNFs are exactly the regenerated bases plus VB's own add-on blocks written from the definitions (EXACT). As the
claim says, **no UNSAT verdict exists yet**: LR(7) at 16 points and weak D(5,7) at 16 points remain OPEN.

## Claim (D1, filed 21:14-21:15)

LR(7) at 16 points holds for every signotope if `c1_rcup7_m16.cnf`, `lrK1_m16.cnf`, `lrK2_m16.cnf` and `lrK3_m16.cnf`
(in `pm1115/d1ev/cnf/`) are all UNSAT; with weak D(5,7) ≤ 15 (DELTA2N) and T4's L1 this would give weak D(5,7) at 16.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vb/claims/d1-lr7m16/`)

1. **The case split.** Let S be a 16-point (5,7)-valid signotope, r ending a 4-cap, l starting a 4-cap, no weak Δ through
   r or through l (an LR(7) failure in the hypothesised form). β(r), α(l) = number of points of a longest cup ending at r
   / starting at l. A 7-cup is a convex 7-set (all its 4-subsets satisfy the convexity condition with all signs +), so
   β(r), α(l) ≤ 6. Cases: β(r) = 6 → S satisfies `c1_rcup7_m16` (ROOT(7)-failure base + "r ends a 6-cup"); else
   α(l) = 6 → the mirror μS (i ↦ 15 − i, (i,j,k) ↦ (15−k, 15−j, 15−i), same sign) is (5,7)-valid (μ reverses each
   4-set's sign sequence, so the signotope axiom and convexity are kept; caps, cups and weak Δs map to caps, cups and
   weak Δs), its rightmost point μ(l) ends a 4-cap and a 6-cup and lies in no weak Δ, so μS satisfies `c1_rcup7_m16`;
   else β, α ≤ 5: (β ≤ 4, α ≤ 4) → `lrK1`; (β = 5, α ≤ 4) → `lrK2`; (β ≤ 4, α = 5) → μS is an LR(7) failure with β and
   α exchanged (μ swaps the roles of l and r, including the hypotheses) → `lrK2`; (β = α = 5) → `lrK3`. The cases are
   exhaustive, so UNSAT of all four CNFs excludes every 16-point LR(7) failure. **Correct.**
2. **Base encoders.** `t3/tools/lr_compact.py` (71 lines, SHA-256 `402970e5…`), read line by line: for an LR(7) failure set
   x = signs, cv = convex 4-sets, B(X) = [X contains a gon] (X not containing both l and r; a gon in X misses one of the
   n smallest points of X), F_K = [K a 4-cap], BadR(D) = [D + r contains a 4-cap] (base: abc and bcr caps), BadL(D) =
   [D + l contains a 4-cap] (base: lab and abc caps; a 4-cap through l is (l,a,b,c)), the 4- and ≥5-point recursions as
   in root_compact; the hypotheses ∨BadR(t), ∨BadL(t) hold, and every row BadR(D) ∨ B((S−r) − D), BadL(D) ∨ B((S−l) − D)
   says "D is not a rooted Δ on that side", true in a failure. So every LR(7) failure satisfies `lc7_m16`. `root_compact.py`:
   same argument (VERIFY_D1_C1SIX.md §3; the code is generic in n).
3. **CNF constructions** (`V/splitcheck.py`, unit `esr-agv-vb-lr7split`): `lr_compact.py 7 16` regenerates
   `898569a8deb75aba1eae79177a5f0bedbb1651779d7ca1c39010b12eb0b3a09f` and `root_compact.py 7 16` regenerates
   `b78f5f51adf1fa55dee3dbd9b3832b98485d4798af86d5d4ecf646a4e4797290` (both equal to the claim). VB's own blocks
   (x_t = 1 + lexicographic index, true = cup): "r ends no k-cup" = for each (k−1)-subset T of {0..14} the clause ∨¬x_t over
   the triples of T ∪ {15}; "l starts no k-cup" the same with {0} ∪ T, T ⊆ {1..15}; "r ends a k-cup" / "l starts a k-cup"
   = a fresh y_T per (k−1)-subset with (¬y_T ∨ x_t) for its triples, then ∨_T y_T. For each file the base is the exact
   clause prefix and the rest equals VB's blocks exactly, in the stated order; headers equal:

   | file | SHA-256 (= claim) | header | blocks after the base |
   |---|---|---|---|
   | `lrK1_m16.cnf` | `0ce89610d12fec8be4628f3fffe363b59754967c13a29550c44ac94b0a5bcb21` | 108,258 / 315,929 | r ends no 5-cup; l starts no 5-cup |
   | `lrK2_m16.cnf` | `593490343d2282d7920dbbec3f614e721952999c36b18579b22be61d05537a10` | 109,623 / 331,218 | r no 6-cup; r a 5-cup; l no 5-cup |
   | `lrK3_m16.cnf` | `8bc9f335e77a48e1f2efebac3c84a963050244a57dc728ff201139d108c70f04` | 110,988 / 346,507 | r no 6-cup; l no 6-cup; r a 5-cup; l a 5-cup |
   | `c1_rcup7_m16.cnf` | `9c7a0da19fea56f73e79e9614ac24c96d481489c66eeb8c813ee07bcc528b83e` | 65,278 / 267,602 | r ends a 6-cup (base rc7_m16) |

4. **Cited, not re-derived:** the step "weak D(5,7) ≤ 15 + L1 + LR(7) at 16 ⇒ weak D(5,7) at 16" (claim t4-lemmas,
   CONFIRMED earlier). D1's controls (`ctl_cup2.py`, `ctl_cup.py`) were not re-run; check 3 replaces them.

## Files (V as above)

| file | SHA-256 |
|---|---|
| `V/splitcheck.py` | `3940fd5f1fb0efdd7a60007110ec46f414cf7de337e54cd54cf9814d811a0650` |
| `V/splitcheck.out` | `d0550bd257eeec54d64ed2a4447da44176ff778278ade9b7466e9949ada5c86b` |

D1's files were only read.
