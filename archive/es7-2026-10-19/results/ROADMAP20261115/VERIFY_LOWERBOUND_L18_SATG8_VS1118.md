# VERIFY_LOWERBOUND_L18_SATG8_VS1118: verdict on claim lb-l18-satg8-31 (verifier VS, 18 November 2026, 03:48-03:50 KST)

(The claim names VERIFY_LOWERBOUND_L18_SATG8.md, which holds VS's verdict on the 36-point claim lb-l18-satg8-36;
hence the suffix _VS1118.)

**Verdict: CONFIRMED at the claimed labels.** S = `l1118/sat31/sl31.txt` (31 integer points):
- (a) S is in general position with **no convex octagon** (largest convex subset 7). EXACT.
- (b) S is **geometrically octagon-saturated**, so **sat_g(8) ≤ 31**. CERTIFIED.

Every clause of the certified CNF is justified by VS's own exact code, independently of l1enc's soundness argument.
Method and code are as in VERIFY_LOWERBOUND_L18_SATG7.md and VERIFY_LOWERBOUND_L18_OCT56.md, with k = 8.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/l18-satg7/`)

1. **Hashes.** The 5 sat31 entries of `l1118/logs/satsmall_sha256.txt` pass.
2. **(a)** VS's convk gives counts 4,495 / 17,915 / 26,021 / 11,050 / 1,295 for m = 3..7 and **0 octagons**
   (`V/satcheck31.out`).
3. **(b) Base `l1enc(S, 8)`** (465 variables, 31,822 clauses, all with 3 literals).
   - **2,155 are exactly VS's own octagon encoding G** (1,295 heptagons; all of G present).
   - The other 29,667 forbid empty patterns (Motzkin): 4,495 = C(31,3) triangle clauses and 25,172 concurrent-line
     clauses. All of them are sign-determined (`V/ot31.out`, 0 failures), so 0 clauses are unexplained.
4. **Added clauses.** All **16,462** are 3-literal empty patterns (Motzkin) matching their comments, and **final =
   base followed by the added clauses**.
5. **Certificate.** VS ran cake_lpr itself (unit `esr-agv-vs-sat31cake`, heap 200) on `sl31g_final.cnf` (47ca0a38…)
   with the kept LRAT (cc4234b4…). The output has **exactly one line `s VERIFIED UNSAT`**.
6. **Control.** `l1enc(S, 8)` alone is SAT (model checked against all 31,822 clauses), so saturation belongs to these
   coordinates, as claimed.

## Not checked

- `satlocal.py`, the search that found S (HEURISTIC; not part of the proof), and the random-point sampling.
- Literature and novelty: DDSZ Thm 4 gives 56; this improves the 36 of lb-l18-satg8-36.
