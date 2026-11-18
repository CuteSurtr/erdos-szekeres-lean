# VERIFY_T1118_ANCHORL_DATA_VS1118: verdict on claim t1118-anchorl-correction (verifier VS, 18 November 2026, 03:59-04:00 KST)

(The claim names VERIFY_T1118_ANCHORL_DATA.md, which holds VS's verdict on t1118-anchorl-data; hence the suffix _VS1118.
The corrected claim t1118-anchorl-strong-data is with VB.)

**Verdict: CONFIRMED (EXACT), with one remark on a count.**
- **The correction is right.** In the 20 n = 6 hostile sets with hostile-list indices 400-419, all 8 of the 872 3-cups
  from l that fail to extend are (0, 7, 14). That cup contains r = 14, so it cannot lie in a weak Δ when r is
  unrootable. **All 864 3-cups from l that avoid r extend to a weak Δ.** So item (d) of t1118-anchorl-strong-data does
  not show a failure of anchoring for cups avoiding r.
- **The added data holds, and more strongly.** In **all 614** right-hostile sets of T2's collection, not only a sample,
  every point a with 1 ≤ a ≤ m − 2 lies in a weak Δ together with l: 9,048 pairs, 0 failures.
- **Remark.** The claim's "46 sampled sets (40 with n = 6, 6 with n = 7) … 593 pairs" does not add up:
  - with `anchor_pairs.py`'s definition (a = 1..m−2), 40 sets with n = 6 (m = 15) give 520 pairs, and any 6 sets with
    n = 7 (m ≥ 17) give at least 90, so at least 610;
  - the sample is not recorded in the claim's files;
  - the property holds on all 614 sets, so the conclusion is unaffected.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/t1118-anchorl/`; own C++ `V/vs_anchork.cpp`, af2849f8…)

- **Input.** `hostile.txt` holds the 614 sets of `t2size/out/all_sets.jsonl` with `rootable[-1] == 0`, in file order.
  So hostile-list index i is line i + 1, and indices 400-419 are all n = 6, m = 15.
- **Method.** For each set, VS enumerated all weak Δs over all 2^m subsets: 4-cap-free (4-cap = all four triples '−')
  and meeting every gon (an (n−1)-set with every 4-subset convex by the sign criterion).
- **Indices 400-419** (`V/anchork_400_419.out`):
  - 872 3-cups (0, a, b) with sign '+';
  - 8 are in no weak Δ, all (0, 7, 14), in 8 sets;
  - 0 non-extending cups avoid r;
  - r lies in 0 weak Δs in all 20 sets;
  - this agrees with the claimant's `out/anchor_k_n3_i6.jsonl`, which lists the same 872 cups and 8 bad (0, 7, 14).
- **All 614 sets** (`V/anchork_all.out`, f3e8a07c…):
  - r lies in 0 weak Δs in every set, i.e. right-hostile confirmed for all 614;
  - **every {l, a} with 1 ≤ a ≤ m − 2 lies in some weak Δ**: 4,524 pairs at n = 6 and 4,524 at n = 7, 0 failures.

## Not checked

- The other items of t1118-anchorl-strong-data, which are VB's.
- The PROVED implication stated there.
