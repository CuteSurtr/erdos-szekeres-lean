**Verdict: CONFIRMED** (claim `lp0-7-false-real-3`, filed by D2; verifier VS, 15 November 2026, 22:21-22:22 KST). Label
EXACT holds. The 20 integer points are a third real (5,7)-valid set on which LP0(7) and ROOT(7) fail: r lies in no weak
Δ, and P0 misses the convex hexagon {9,10,11,14,16,19}. LR(7) and weak D(5,7) hold on it, because l lies in 3,655
weak Δs. Its order type differs from those of `lp0-7-false-real` and `lp0-7-false-real-2` (1,042 convex hexagons
against 1,011 and 1,055). Every number was recomputed from the coordinates by VS's own code.

# VERIFY_LP0_7_FALSE_REAL_3: a third real 20-point counterexample to LP0(7)

**Input.** `pm1115/d2/hit/lp0_7_real20_t1it4_b.json`, field `P`, SHA-256
`9e5efcffa4748874ae04cd11f0939d0dff8e86b78c35565479624bfec094373d` (as claimed), with |coordinate| ≤ 533,029.

**Method.** `vs_lp0real3.py` is the script of VERIFY_LP0_7_FALSE_REAL.md, with the input, the hexagon, the listed
caps and the comparison block changed. It uses VS's `vslib.py` and the brute force `bf_delta.cpp` over all 2^20
subsets.

| # | check | result |
|---|---|---|
| 1 | x strictly increasing; no collinear triple; signotope axiom; the 4-point sign rule equals geometry on all 4,845 4-subsets | yes |
| 2 | 5-caps / convex 7-sets (backtracking and brute force over all 15,504 / 77,520 subsets) | **0 / 0**, so the set is (5,7)-valid |
| 3 | 4-caps; convex hexagons; 4-caps ending at r = 19 | **295; 1,042; 154** (as claimed) |
| 4 | P0 | **{0,1,2,3,5,6,12,13,15,17,18}** (4-cap-free) |
| 5 | hexagons missed by P0 | exactly **1**: {9,10,11,14,16,19}. It is convex and disjoint from P0, and the six listed 4-caps (0,5,6,9), (0,2,7,10), (0,2,7,11), (0,5,12,14), (0,2,15,16), (0,1,4,19) are caps ending at its six points |
| 6 | weak Δ through r (exhaustive DFS; brute force over 2^20 subsets) | DFS: **none**. Brute force: 6,694 weak Δs, **0 through r**, **3,655 through l = 0** |
| 7 | S − {5, 6, 9} vs T1's block `t1/r7c17/feasible/m17_it4_real.json` (signs computed by VS from its coordinates) | equal (SHA-256 `8e287c59…`, the same block as in claim 2) |

**Not checked.** The origin (BFP-CEGAR and realize_sig) and the filer's checkers; the statement rests on the
coordinates alone.

**Files** (`/home/jay/research/data/roadmap-20261115/pm1115/vs/lp0-7-false-real-3/`):

| file | SHA-256 |
|---|---|
| `vs_lp0real3.py` | `fdf8a1f53a20356aca6526d5157d3cacba67163db6589da4e7f9c92e6b266b9b` |
| `vs_lp0real.json` | `41e60a84d0fc937cab06c8fe519de1fe9badc55babc0a568514423ac1967c547` |
| `masks.txt` | `1321fec5a2b75086cedb10016ea6564d6aed7824611603e1874c7fb4e2413e3a` |
| `bf_delta.out` | `227e0caf20c21405e6d8834835a707228a8168e1e37e18bd2b019df8e76a833c` |

Everything ran in the foreground in under 1 s. No unit was started and no git action was taken.
