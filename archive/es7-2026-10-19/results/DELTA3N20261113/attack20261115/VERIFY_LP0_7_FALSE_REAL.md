**Verdict: CONFIRMED** (claim `lp0-7-false-real`, filed by D2; verifier VS, 15 November 2026, 21:12-21:13 KST). Label
EXACT holds. The 20 integer points form a real (5,7)-valid set whose rightmost point lies in no weak Δ, while P0 misses 6
convex hexagons. So **LP0(7) is false for a real point set with 20 points**, and the same set refutes ROOT(7). LR(7)
and weak D(5,7) hold on it, because l lies in 4,040 weak Δs. Every number was recomputed from the coordinates alone by
VS's own code.

# VERIFY_LP0_7_FALSE_REAL: a real 20-point counterexample to LP0(7)

## Input

`pm1115/d2/hit/lp0_7_real20.json`, field `P`, SHA-256 `dd7291027c456978936f6bd685ff71a73772038f877b3cd9abd9de0225d0af2b`
(as claimed). It has 20 integer points with |coordinate| ≤ 28,611.

## Checks (own code `vs_lp0real.py` on VS's `vslib.py`, exact Python integers; brute force `bf_delta.cpp`)

| # | check | result |
|---|---|---|
| 1 | x strictly increasing; no collinear triple (all 1,140 orientations nonzero) | yes |
| 2 | the signs satisfy the signotope axiom; the sign rule for convex 4-sets equals the geometric test (no point inside the triangle of the other three) on all 4,845 4-subsets | yes / yes |
| 3 | 5-caps (backtracking, and brute force over all 15,504 5-subsets) | **0** / 0 |
| 4 | convex 7-sets (backtracking, and brute force over all 77,520 7-subsets) | **0** / 0, so S is (5,7)-valid |
| 5 | 4-caps; convex hexagons (gons); 4-caps ending at r = 19 | 312; 1,011; **165** |
| 6 | P0 (points that end no 4-cap) | **{0,1,2,3,5,6,11,12,17,18}**, as claimed; it is 4-cap-free |
| 7 | gons missed by P0 | **6**: {7,8,9,13,15,16}, {7,8,10,13,15,16}, {7,8,13,14,15,16}, {7,9,10,13,15,16}, {7,9,10,13,15,19}, {7,9,10,13,16,19} |
| 8 | {7,8,9,13,15,16} is convex and disjoint from P0; the six listed 4-caps (0,5,6,7), (0,2,7,8), (0,2,7,9), (1,5,12,13), (1,5,12,15), (0,2,15,16) are caps | yes / yes |
| 9 | weak Δ through r. DFS: complete branching on an unhit gon, adding only points that keep the set 4-cap-free. Brute force: all 2^20 subsets, 4-cap and gon bitmasks | DFS: **none**. Brute force: 8,734 weak Δs in all, **0 through r = 19**, **4,040 through l = 0** |
| 10 | optional: S − {5, 6, 12} | its sign string equals `r7/root7_real17.json` `signs` (SHA-256 `33825503…`, = the file's `signs_sha256`); R7's coordinates give the same string |

So r is unrootable (ROOT(7) fails), and P0 does not meet every gon, so P0 is not a weak Δ. That is exactly a failure of
LP0(7) ("r lies in some weak Δ, or P0 meets every gon"; THEORY_1115PM.md §0, §1.4). Also, r ends a 4-cap, so the
version of LP0 with the hypothesis "r ends a 4-cap" fails too. Since l = 0 lies in 4,040 weak Δs, LR(7) and weak D(5,7)
hold on S. One example is {0,1,2,3,5,6,11,13,17,18}, re-checked as a weak Δ.

## Controls

- `vslib.py` self-test: random point sets, with the DFS weak-Δ search against brute force over all subsets and the
  4-point rule against geometry (PASS, 19:00).
- Here the DFS verdict and the C++ brute force agree, and the backtracking counts of items 3-4 equal brute force.

## Not checked

The claim's origin story: the BFP-CEGAR model, its missing BFP certificate (HiGHS; never evidence) and the
realize_sig run. The filer's three checkers were not run or read. None of this is needed: the statement rests on the
coordinates alone.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/vs/lp0-7-false-real/`)

| file | SHA-256 |
|---|---|
| `vs_lp0real.py` | `4c7a7500c9a633f3ec186d98acd95a57bdeb330776caf9a9f5eb8bb51182391d` |
| `../vslib.py` | `5af879109f9f9543602a45d63f752960c5e8135aed36147ffe04bea73efa7205` |
| `bf_delta.cpp` | `642dcf5c4ee7de1df08e1f27089edb2395e64d319d2161904984feba7027523a` |
| `vs_lp0real.json` (all values) | `b854e068052a8c1ffe435ecc7770c872cff06c8d01ba73c02c58538162adf2fe` |
| `masks.txt` (4-cap and gon bitmasks) | `1d9699a50f90691870850636c66282188aedf25cfba4d571a8e7250e52bcb3c8` |
| `bf_delta.out` | `39a6a50e6830b6bb45ae49a128353a466aca34c7ab87167a2806a28046387095` |

Rerun: `python3 -I vs_lp0real.py; g++ -O2 -o bf_delta bf_delta.cpp; ./bf_delta masks.txt`. Together they take under
1 s. No unit was started and no git action was taken.
