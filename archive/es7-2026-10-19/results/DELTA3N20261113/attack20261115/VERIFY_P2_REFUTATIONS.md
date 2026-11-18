**Verdict: CONFIRMED** (claim `p2-witness-refutations`, verifier V2, 15 November 2026, 17:14-17:16 KST). Label EXACT
is correct. All four refutations (H4, H2, H5U, H6) reproduce from the integer coordinates with V2's own code. There is
one extra detail for H2: P0 misses a third hexagon, {5,7,9,12,13,14}, besides the two listed. This does not affect
the refutation.

# Independent check: four explicit-witness strengthenings of LP0 are false (PROOF_LP0_ATTEMPT_P2.md §4)

I read the version of PROOF_LP0_ATTEMPT_P2.md with SHA-256 `d358c826…8517`.

**Definitions.** THEORY_1115PM.md §0:
- R¹: points ending a 4-cap; P0 = S − R¹;
- L¹: points starting a 4-cap; Q0 = S − L¹;
- gon: convex (n−1)-set by the 4-point rule; weak Δ: 4-cap-free and meets every gon;
- terminal-safe: every 3-cap (a,b,c) inside has (b,c) ending a 4-cap of U;
- β(v): the number of points of a longest cup of U ending at v;
- mirror: x → −x, with the order reversed.

**Code.** `/home/jay/research/data/roadmap-20261115/pm1115/v2/p2-witness-refutations/check_p2_v2.py`
(`8db9cfe17d494aebed1ad0cfbdb48ccad27e016136da5507efb1c9354dd42b1d`), with `v2lib.py` (`7c8b1ee0…`). Its output is
`p2_check.json` (`60208c9e…`). It ran in about 1 s on one thread.
- Everything is computed from the integer coordinates: orientations, caps and cups by the all-triples definition, and
  validity (signotope axiom, no 5-cap, no convex n-set).
- Every gon used was cross-checked with the cup/cap-split convexity test.
- Subsets were enumerated exhaustively.

## Results

- **H4: "P0 ∪ Q0 meets every gon" is FALSE.**
  - Set: `t4/lay/min_LRB_n8.json` (`81f033e4…`), 25 points, and its mirror. Both are (5,8)-valid and have 1,013
    heptagons each.
  - **3 heptagons inside R¹ ∩ L¹ in each orientation**: {8,9,12,14,16,20,21}, {8,9,12,14,17,20,21} and
    {8,9,12,14,18,20,21}, and in the mirror {3,4,6,10,12,15,16}, {3,4,7,10,12,15,16} and {3,4,8,10,12,15,16}.
  - The claim's example is among them. The equivalence "no gon inside R¹ ∩ L¹ ⟺ P0 ∪ Q0 meets every gon" is
    immediate.
- **H2: "if P0 misses a gon, Q0 ∪ X is a weak Δ for some X ⊆ P0 − Q0" is FALSE.**
  - Set: the mirror of `t4/lay/min_LR_n7.json` (`93c47864…`), 15 points, (5,7)-valid, with 94 hexagons.
  - P0 = {0,1,2,3,6,8,11} and Q0 = {1,3,8,9,10,11,12,13,14}, as stated, so P0 − Q0 = {0,2,6}.
  - P0 misses the hexagons {4,5,10,12,13,14}, {4,7,9,12,13,14} and also {5,7,9,12,13,14}.
  - **None of the 8 sets Q0 ∪ X is a weak Δ.**
  - {4,12,14} is a weak Δ, so r = 14 is rooted, as stated.
- **H5U: "a gon of U inside R¹(U) gives a terminal-safe weak Δ of U" is FALSE.**
  - Set: S = `t1/tspm6_real15.json` (`142707d7…`), (5,6)-valid, with U = S − r of 14 points and 190 pentagons.
  - {3,5,6,8,12} is a pentagon of U inside R¹(U). It is the only such pentagon.
  - U has 1,901 weak Δs and **0 terminal-safe** ones (exhaustive over 2^14 subsets).
- **H6: "… gives a weak Δ of U with non-increasing cup ranks" is FALSE.**
  - Sets: the mirrors of all 21 real ROOT(6) sets `t1/real/m15_it*_real.json`, each (5,6)-valid.
  - In each, U = S − r has 6 gons inside R¹(U), and the same 6 lie inside R¹(S). So the hypothesis holds in either
    reading.
  - **0 weak Δs of U with β(v) ≥ β(w) for all v < w in Δ.** I counted by forbidding every pair v < w with β(v) < β(w),
    and enumerating all subsets.

**Comparison** (read after my check). The filer's `p2/refute_check.out.json` (`b83affc6…`) gives the same H4 counts and
examples in both orientations. I did not compare the other entries line by line. The record's remark "730 ENV# Δs" for
H5U is not part of the claim and was not checked.
