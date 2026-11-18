**Verdict: CONFIRMED** (claim `lp0-7-realblock-nonreal`, verifier V2, 15 November 2026, 17:46-17:49 KST). Label
EXACT is correct.
- All 21 certificates are valid for the chirotopes I rebuilt from the scan's sign strings.
- 20 use no V, so those models have no realization by any planar point configuration.
- 1 uses V (block r7, pattern onnoooooooooooooooo), so that model has no realization with x increasing in the index
  order.

None of the 21 models therefore has an x-sorted real realization.

# Independent check: the 21 real-block LP0(7) extension models are not realizable

**Definitions.** These are as in claims `root6-m15-main-nonrealizable` and `root7-m17-nonreal-1` (both V2 CONFIRMED;
[VERIFY_ROOT6_M15_NONREAL.md](VERIFY_ROOT6_M15_NONREAL.md)):
- points p_i = (1, x_i, y_i) and V = (0,0,1), with [a,b,V] = x_b − x_a;
- lexicographic signs, `+` = cup, with the parity rule;
- the 3-term GP identity, giving log|T_odd| > log|T_other|;
- positive integer multipliers summing to the zero form give 0 > 0.

**Code.** `/home/jay/research/data/roadmap-20261115/pm1115/v2/lp0-7-realblock-nonreal/check_batch_v2.py`
(`540ce2c5df96f4ae6cb6c17fbf61b4b3feac68cd906b28cb47ca8623fb2880a8`). Its output is `batch_check.jsonl`
(`1bfd0e19…`). It uses `bfp_v2core.py`, a byte copy of V2's validated BFP checker (`645ccfab…`, with GP-identity,
real-configuration and negative controls in VERIFY_ROOT6_M15_NONREAL.md), and `v2lib.py` (`7c8b1ee0…`). R7's tools
were not read.

## Checks

1. **Selection.** The scan `p2/lp0scan_k2.jsonl` has SHA-256 `bedfd8c0…8d28453`, as stated, and 1,535 records. The
   records with `sat: true` and block `r7/root7_real17.json` or `t1/r7c17/feasible/m17_it4_real.json` number **21**:
   **11 + 10**, as stated.
2. **Identity.** Each record's 969-character `signs` equals the matching `r7/lp0/batch/W_<block>_<pattern>.json`, and
   each certificate's `model_sha` is the SHA-256 of those signs.
   - The three W files of claim `lp0-7-false-abstract` (r7, patterns oonn…, onn… and oonon…) are byte-equal in signs
     to `p2/lp0cex/w19_real17_*.json`.
3. **Certificates.** For each model I rebuilt the chirotope from the signs: 19 points, or 20 elements with element 19 =
   V and `+` on every triple containing it. Each certificate's `sig` equals my rebuild. Then for every item:
   - five distinct elements in range;
   - a positive integer multiplier;
   - the stated odd term opposite in sign to both other terms;
   - ±mult accumulated on unordered triples.

   **All totals are 0 in all 21: accepted 21/21.** There are 20 `noV` certificates and 1 `withV`
   (r7/onnoooooooooooooooo), which really uses V. The certificates have **588 to 746 items**, as stated.
4. **Bonus: what the models are.** All 21 are (5,7)-valid: 0 signotope violations, no 5-cap, no convex 7-set.
   - In each, r = 18 lies in **no** weak Δ (exhaustive over 2^19 subsets).
   - Each embeds its real 17-point block: the points marked `o` in the pattern have exactly the block's orientation
     signs, computed from its integer coordinates.
   - So all 21 are abstract right-hostile 19-point extensions of real blocks, and none of them is realizable. This
     includes W of `lp0-7-false-abstract`.

**Not checked.**
- The context remark "every first new point's cell is already empty (LP slack < 0)": a search statement, HiGHS-based,
  never evidence.
- `batch.jsonl` (`6c5593bb…`, equal to the claim) was hashed but not used.
