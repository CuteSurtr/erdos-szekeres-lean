# VERIFY_NOV_ETV8_CORRECTION: verdict on claim nov-etv8-corollaries-correction (verifier VS, 18 November 2026, 03:24-03:27 KST)

**Verdict: CONFIRMED (PROVED).** Item (iv) of `nov-etv8-corollaries`, N(8; 7, 8) ≤ 401, is true but carries no
information, and it is correctly withdrawn. Items (i)-(iii) stand as the correction says.

## Checks

- **The argument.** A set counted by N(8; a, b) is in general position with no convex octagon. By the definition of
  ES(8), such a set has at most ES(8) − 1 points.
- **The bounds that follow.**
  - RESULTS.md row A1 states ES(8) ≤ 310, Lean-checked on 10 Nov and not refereed. So N(8; 7, 8) ≤ 309 < 401, and
    likewise ≤ 307 from the unrefereed ES(8) ≤ 308 chain.
  - Schroeder's unrefereed ES(8) ≤ 319 gives 318.
  - The refereed Mojarrad–Vlachos bound C(2n−5, n−2) − C(2n−8, n−3) + 2 is 462 − 56 + 2 = 408 at n = 8, which gives only
    407. So their direct (7, 8) ≤ 406, listed in WATCH_1118 §2a, is the best refereed value.
- **Items (i)-(iii).** Recomputed: (i) 56 + 56 = 112, (ii) 65 + 112 = 177, (iii) 112 + 112 = 224, and (iv) 177 + 224
  = 401.
  - The cup–cap values C(a+b−4, a−2) for (6,7), (6,8), (7,7) and (7,8) are 126, 210, 252 and 462.
  - (i) and (ii) lie below both their cup–cap values and 309, so they stand.
  - (iii) = 224 lies below 252 and 309 but is weaker than Schroeder's unrefereed 193, as stated.
- **"Changes the best public bound only for (8; 7, 8)".** The WATCH_1118 §2a list already has (8, 8) ≤ 318 (Schroeder).
  For the other listed pairs, the existing values (cup–cap 126/210/252, Schroeder 193, Baek 22) are already below 318.
  So only (7, 8), at 406, improves, to 318 (unrefereed).
- **Records.** The updates named in the claim are present:
  - WATCH_1118.md, Remark at lines 147-151: "true but empty … Do not quote 401";
  - NOVELTY_MAP_1118.md row B11: item (iv) withdrawn.
- The parent claim's verdict (VB CONFIRMED 03:15) covers the arithmetic and the endpoint-split lemma. VS did not re-check
  those beyond the recomputation above.

Not checked: the literature statements themselves (Mojarrad–Vlachos 406, Schroeder 319 and 193). They are taken as
quoted in WATCH_1118 §2a, which is the record's own literature check.
