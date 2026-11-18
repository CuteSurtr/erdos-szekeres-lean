# VERIFY_T1118_CUPANCHOR_VS1118: verdict on claim t1118-wd2n1 (Corollary A4; verifier VS, 18 November 2026, 03:21-03:24 KST)

(The claim names VERIFY_T1118_CUPANCHOR.md, which already holds VS's verdict on its parent claim t1118-cupanchor;
hence the suffix _VS1118.)

**Verdict: CONFIRMED (PROVED).**
- For n ≥ 6, every (5,n)-valid signotope S with |S| ≤ 2n − 1 has a weak Δ.
- At |S| = 2n, a weak Δ exists unless the longest cup of S has exactly n − 2 points.

The two-case proof is correct. Its inputs are both CONFIRMED:
- Theorem A, claim `t1118-cupanchor`, VS CONFIRMED 03:13;
- Corollary SD, claim `p1-cupext`, V2 CONFIRMED.

## Proof check

- (5,n)-valid means no convex n-set, so every cup has at most n − 1 points and Theorem A applies to S.
- **Case 1: |S| ≤ 2n − 1 and S has an (n−2)-cup K** (in particular whenever the longest cup has n − 2 or n − 1 points).
  Then |S − K| ≤ (2n − 1) − (n − 2) = n + 1, and Theorem A gives a weak Δ K ∪ X with |X| ≤ 1.
- **Case 2: S has no (n−2)-cup.** Corollary SD (PROOF_LR_ATTEMPT_P1.md §2) says P0 (and Q0) is a weak Δ, for any size.
- **|S| = 2n:**
  - an (n−1)-cup K gives |S − K| = n + 1, and Theorem A applies;
  - no (n−2)-cup is Case 2;
  - what remains is exactly "longest cup = n − 2", which the statement excludes.

## Control (own exact code: `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/t1118-wd2n1/vs_wd2n1.py`, output `wd2n1.out`)

- Setup: random subsets with n + 2 .. 2n points of the real (5,6)-valid set `t1/real/m15_it8_real.json` (60 subsets,
  n = 6) and the real (5,7)-valid block `d2/blocks/r7real.json` (12 subsets, n = 7).
- Method: weak Δ existence by enumerating all 2^|T| subsets, convexity by point-in-triangle; validity of each subset
  asserted.
- **Every subset the corollary covers (71) has a weak Δ: 0 violations.**
- The one excluded subset (14 points, n = 7, longest cup 5 = n − 2) also has one. The statement makes no claim there.

Files: vs_wd2n1.py e681857a7e8f36f9…, wd2n1.out 8cb96d7898780a69….
