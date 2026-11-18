**Verdict: CONFIRMED** (claim `lp0-7-false-real-2`, filed by D2; verifier VS, 15 November 2026, 22:00-22:02 KST). Label
EXACT holds. The 20 integer points are a second real (5,7)-valid set on which LP0(7) and ROOT(7) fail: the rightmost
point lies in no weak Δ, and P0 misses 5 convex hexagons. LR(7) and weak D(5,7) hold on it, because l lies in 3,329
weak Δs. It is a different order type from the set of `lp0-7-false-real`: it has 1,055 convex hexagons against 1,011,
and the number of convex hexagons is invariant under relabelling and reflection. Every number was recomputed from the
coordinates by VS's own code.

# VERIFY_LP0_7_FALSE_REAL_2: a second real 20-point counterexample to LP0(7)

## Input

`pm1115/d2/hit/lp0_7_real20_t1it4.json`, field `P`, SHA-256
`3692cfc9969620f686e4f253ebfe42e9340ba056730de1593c5a86334306bce9` (as claimed). It has 20 integer points with
|coordinate| ≤ 116,317.

## Checks (own code `vs_lp0real2.py` = `vs_lp0real.py` of VERIFY_LP0_7_FALSE_REAL.md with the input and comparison set changed; VS's `vslib.py`; brute force `bf_delta.cpp`)

| # | check | result |
|---|---|---|
| 1 | x strictly increasing; no collinear triple | yes |
| 2 | signotope axiom; the sign rule for convex 4-sets equals the geometric test on all 4,845 4-subsets | yes / yes |
| 3 | 5-caps (backtracking; brute force over 15,504 5-subsets) | **0** / 0 |
| 4 | convex 7-sets (backtracking; brute force over 77,520 7-subsets) | **0** / 0, so S2 is (5,7)-valid |
| 5 | 4-caps; convex hexagons; 4-caps ending at r = 19 | **326; 1,055; 159** (as claimed) |
| 6 | P0 | **{0,1,2,3,5,6,11,12,17,18}** (4-cap-free) |
| 7 | hexagons missed by P0 | **5**: {7,8,9,13,15,16}, {7,8,10,13,15,16}, {7,8,13,14,15,16}, {7,9,10,13,15,16}, {7,9,10,13,15,19} |
| 8 | {7,8,9,13,15,16} is convex and disjoint from P0; the six listed 4-caps are caps | yes / yes |
| 9 | weak Δ through r (exhaustive DFS; brute force over all 2^20 subsets) | DFS: **none**. Brute force: 6,768 weak Δs, **0 through r**, **3,329 through l = 0** |
| 10 | S2 − {5, 6, 12} vs T1's real block `t1/r7c17/feasible/m17_it4_real.json` (that file has no sign field, so VS computed the signs from its coordinates) | equal (sign string SHA-256 `8e287c59…`) |
| 11 | S2 vs S (`lp0_7_real20.json`) | the labelled sign vectors differ in 10 triples, and S2's mirror differs from S as well. The order types differ: the hexagon counts are 1,055 vs 1,011 |

So r is unrootable and P0 is not a weak Δ, which means LP0(7) fails, and ROOT(7) fails too. LR(7) and weak D(5,7) hold
on S2.

## Not checked

The origin (BFP-CEGAR model and realize_sig run) and the filer's three checkers. The statement rests on the coordinates
alone.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/vs/lp0-7-false-real-2/`)

| file | SHA-256 |
|---|---|
| `vs_lp0real2.py` | `e67e6076b8cb6484170d4222c5444b01219a1981bee4bb9968f24fa59e8ca5ed` |
| `vs_lp0real.json` (all values) | `fbf3555e346d2e9429cba57c400c33902032294b671124d72569d5f04979e1be` |
| `masks.txt` | `0fddd34408f7d1e5c5b37cfdfd04a2b5a0a9ae4a3cd891525deec7db403139e3` |
| `bf_delta.out` | `69c76305f322b515c2f552a1d89cea925cfce7dc282d36307e8c28ce86270b61` |
| `../lp0-7-false-real/bf_delta.cpp`, `../vslib.py` | `642dcf5c…`, `5af87910…` (as in VERIFY_LP0_7_FALSE_REAL.md) |

Everything ran in the foreground in under 1 s. No unit was started and no git action was taken.
