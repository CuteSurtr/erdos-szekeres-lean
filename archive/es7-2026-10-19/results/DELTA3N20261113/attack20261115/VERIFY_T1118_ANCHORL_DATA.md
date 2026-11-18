# VERIFY_T1118_ANCHORL_DATA: verdict on claim t1118-anchorl-data (verifier VS, 18 November 2026, 03:40-03:42 KST)

**Verdict: CONFIRMED (EXACT), as claimed. The conjecture ANCHOR-L itself is not claimed and not judged.** VS's own code
(not `anchor_l.py`) reproduces both parts of the claim:
- ANCHOR-L holds on all 614 right-hostile sets of T2's collection, with the claimed smallest |X|;
- the mirror of the 13-point model is a counterexample to anchoring at l in general.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/t1118-anchorl/`)

1. **Selection.** `t2size/out/all_sets.jsonl` has 1,440 sets; 614 have `rootable[-1] == 0`:
   - n = 6, m = 15: 348;
   - n = 7, m = 17: 45; m = 18: 1; m = 19: 127; m = 20: 93.

   They are given as sign strings over lexicographic triples ('+' = cup).
2. **Own exhaustive check** (`V/vs_anchorl.cpp`, C++ bitmasks, all definitions from the signs; output `V/anchorl.out`,
   one line per set). Definitions:
   - convex 4-set: s(abc) = s(abd) and s(acd) = s(bcd);
   - gon: (n−1)-set with every 4-subset convex;
   - 4-cap: all four triples '−';
   - (n−1)-cup: all triples '+';
   - weak Δ: 4-cap-free and meeting every gon.

   Results:
   - **r lies in 0 weak Δs in all 614 sets.** All 2^(m−1) sets containing r were enumerated for every set, not just a
     sample.
   - All 614 satisfy ANCHOR-L's hypotheses: r ends a 4-cap and l starts a 4-cap. These flags agree with T2's metadata.
   - Every set has at least one (n−1)-cup K with min K = l.
   - Searching X ⊆ S − K in increasing size, **some K ∪ X is a weak Δ in all 614 sets.**
   - Least |X|:

     | n | m | 1 | 2 | 3 |
     |---|---|---|---|---|
     | 6 | 15 | – | 296 | 52 |
     | 7 | 17 | 45 | – | – |
     | 7 | 18 | 1 | – | – |
     | 7 | 19 | 100 | 27 | – |
     | 7 | 20 | 14 | 79 | – |

     So the least |X| is in {2, 3} at n = 6 and in {1, 2} at n = 7. The totals equal the sum of the blocks of the
     claimant's `anchor_l_all_summary.txt`.
   - Control: the first sets (D2's real blocks) reproduce VS's earlier exact counts, e.g. r7it3 with 277 gons and 173
     4-caps (VERIFY_CN_LP0_EXT1.md).
3. **Mirror statement** (`V/mirror13.out`, Python from the signs).
   - `t1118/models/c1allcups_6_13.json` is a 13-point signotope (axiom checked on all 4-sets) and is (5,6)-valid. It has
     672 weak Δs, 65 of them through r (so r is rootable), and its only 5-cup ending at r, (0,5,6,9,12), lies in none.
   - Its mirror (i ↦ 12 − i, (a,b,c) ↦ (12−c,12−b,12−a), same sign) is (5,6)-valid. **Its only 5-cup starting at l,
     (0,3,6,7,12), lies in 0 of its 672 weak Δs.** Anchoring at l therefore fails without ANCHOR-L's hypothesis: in the
     mirror, r lies in 389 weak Δs.

## Not checked

- The running full CNF for ANCHOR-L(6) at 15 points (unit `esr-agt-anchorl6full`), which the claim does not cover.
- That ANCHOR-L implies C2(n) and LR(n): the claim says so in passing, and nothing is claimed for it.

Files (SHA-256): cc1cca5587ab006b1a56c3c7517cb7ea3b9c57a0a6e95eea0826f61573f5b885 vs_anchorl.cpp;1b593de45a72a30ba3f9e6305be674cb2ab77ecae2c3cd2d406c35fe9311c316 anchorl.out;b1acebf9d39a3afcabf9c4f19169d4bcd22b3a60be3d5b25f8c3f65668de9180 hostile.txt;2c168044ed0b8374b93d0daef3b4d7c42fa14777c1cdfb39e274c767a57f7309 mirror13.out;
