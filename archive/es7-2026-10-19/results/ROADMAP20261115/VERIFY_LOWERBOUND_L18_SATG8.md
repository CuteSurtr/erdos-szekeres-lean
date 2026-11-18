# VERIFY_LOWERBOUND_L18_SATG8: verdict on claim lb-l18-satg8-36 (verifier VS, 18 November 2026, 03:25-03:28 KST)

**Verdict: CONFIRMED at the claimed labels.** S = `l1118/sat36/g5_m7_f1_k8_s1.txt` (36 integer points):
- (a) S is in general position and has **no convex octagon**; its largest convex subset has 7 points. EXACT.
- (b) S is **geometrically octagon-saturated**, so sat_g(8) ≤ 36. CERTIFIED.

Every clause of the certified CNF is justified by VS's own exact code, without using l1enc's soundness. The method and
code are those of [VERIFY_LOWERBOUND_L18_SATG7.md](VERIFY_LOWERBOUND_L18_SATG7.md) and
[VERIFY_LOWERBOUND_L18_OCT56.md](VERIFY_LOWERBOUND_L18_OCT56.md), with k = 8.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/l18-satg7/`)

1. **Hashes.** `.txt`, `.pts`, `.cnf`, `_added.txt` and `_final.cnf` pass `sha256sum -c` against
   `l1118/logs/satsmall_sha256.txt`.
2. **(a)** `vs_convk`, 128-bit, on the x-sorted copy: general position, convex m-gon counts 7,140 / 33,270 / 58,922 /
   36,140 / 6,065 for m = 3..7, **0 octagons**.
3. **(b) Base CNF `l1enc(S, 8)`** (630 variables, 52,797 clauses, all with 3 literals; `V/satcheck36.out`).
   - **5,265 clauses are exactly VS's own exact octagon encoding G** (`vs_gclauses2` k = 8: 6,065 heptagons, all of G
     present).
   - The other **47,532 forbid geometrically empty patterns** (exact Motzkin test), so **0 are unexplained**.
   - The empty ones are 7,140 = C(36,3) triangle clauses and 40,392 concurrent-line clauses. All of them are decided
     empty by the orientation signs alone (`vs_ot_invariant.py`, 0 failures).
4. **Added clauses.** All **20,543** are 3-literal clauses forbidding geometrically empty patterns (Motzkin), each
   matching its comment, and **final = base followed by the added clauses**.
5. **Certificate.** VS ran cake_lpr itself (unit `esr-agv-vs-sat36cake`, heap 200, peak 128 MB) on `_final.cnf`
   (8ea6d03b…) with the kept LRAT (26ffdc99…, decompressed). The output has **exactly one line `s VERIFIED UNSAT`**.
6. **Control.** `l1enc(S, 8)` alone is SAT: CaDiCaL exit 10, and the model satisfies all 52,797 clauses. So, as
   claimed, saturation is a property of these coordinates, not of the order type.

## Not checked

- The Z[ζ5] rounding provenance and the random-point sanity sampling.
- The literature context (DDSZ Thm 4: 56; `lb-l18-otsat-nonmax`: 51), and novelty.
