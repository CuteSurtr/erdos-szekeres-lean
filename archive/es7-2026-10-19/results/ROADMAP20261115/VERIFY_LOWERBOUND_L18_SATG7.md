# VERIFY_LOWERBOUND_L18_SATG7: verdict on claim lb-l18-satg7-21 (verifier VS, 18 November 2026, 03:14-03:18 KST)

**Verdict: CONFIRMED at the claimed labels**, for the 21-point headline set and for all five further instances:
- **The 21-point set S (`sat21/g5_m4_f1_k7_s2.txt`) is in general position, has no convex 7-gon (largest convex
  subset 6), and is geometrically 7-gon-saturated**, so sat_g(7) ≤ 21.
- The three 24-point sets are geometrically saturated in the same way.
- The two 26-point sets are saturated **in every realization of their labelled order type**.

**Independence.** Every clause of every certified CNF is justified by VS's own exact code, so the l1enc soundness
argument is not needed:
- base clauses are clauses of VS's octagon-type encoding G for k = 7, or geometrically empty patterns;
- for the 26-point sets, each empty pattern is shown empty **from the orientation signs alone**;
- the added clauses are exactly checked empty patterns;
- cake_lpr, re-run by VS, accepts all six certificates.

Not checked: the novelty of sat_g(7) ≤ 21 (literature) and the provenance of the coordinates (the Z[ζ5] rounding);
neither affects the statements.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/l18-satg7/`; L = `pm1115/l1118/`)

1. **Hashes.** `sha256sum -c L/logs/satsmall_sha256.txt` passes for every set, CNF, added-clause and final file. The
   one mismatch is `bin/satsearch.sh`, which is not a claim file.
2. **(a) Convex counts** (`vs_convk`, 128-bit; the x-sorted copy, since the labels are not in x-order; `V/satcheck.out`).
   All six sets are in general position, with **largest convex subset 6 and 0 convex 7-gons**.

   | set | n | convex m-gons, m = 3..6 |
   |---|---|---|
   | g5_m4_f1_k7_s2 | 21 | 1,330 / 3,425 / 3,294 / 900 |
   | g6_m4_f0_k7_s2 | 24 | 2,024 / 6,396 / 8,316 / 3,949 |
   | g4_m6_f0_k7_s3 | 24 | 2,024 / 6,334 / 7,376 / 2,294 |
   | g4_m6_f0_k7_s4 | 24 | 2,024 / 5,822 / 4,972 / 1,174 |
   | a5_m5_c1_k7_s1 | 26 | 2,600 / 7,785 / 7,905 / 2,035 |
   | a5_m5_c1_k7_s2 | 26 | 2,600 / 7,915 / 8,035 / 2,145 |

3. **Own encoding G for k = 7** (`V/vs_gclauses2.cpp`; the encoder of VERIFY_LOWERBOUND_L18_OCT56 with label mapping).
   - Rule: p lies on a convex 7-gon of S + p iff, for some convex hexagon of S (CCW) and some edge, p is beyond that edge
     and inside the lines of the two adjacent edges.
   - It reproduces the k = 8 output for d56 byte for byte.
   - Exactness control with labels shuffled (`V/vs_g_ctl2.py`): 200 random real (S, p), 0 mismatches against exact
     k-gon counts.
4. **(b) Base CNF = l1enc(S, 7), clause by clause** (`V/vs_satcheck.py`).
   - Every clause has 3 literals over X(a,b) = [orient(a,b,p) > 0], variable 1 + lexicographic rank of the labels a < b.
   - Each clause is **either a clause of G (all of G occurs) or a geometrically empty pattern** (exact Motzkin test);
     **0 are unexplained**.
   - 21 points: 1,440 G + 8,512 empty = 9,952.
   - 24 points: 3,114 / 2,980 / 1,996 G + 13,112 empty each.
   - 26 points: 3,005 / 3,065 G + 16,952 empty each.
5. **The empty base clauses are order-type invariant** (`V/vs_ot_invariant.py`, which uses only the signs of triples of
   S).
   - **Triangle type**, exactly C(n,3) per set (1,330 / 2,024 / 2,600): lines ab, ac, bc, and the pattern says p is
     strictly beyond all three edges of the triangle. That pattern is empty for every triangle.
   - **Concurrent type** (7,182 / 11,088 / 14,352): lines a b_i through one point a. With v_i = s_i(b_i − a), where s_i
     is the forbidden sign of orient(a, b_i, p), the open half-planes meet iff the v_i lie in an open half-plane. VS
     verified that det(v1,v2), det(v2,v3), det(v3,v1) all have one sign, i.e. the v_i span positively, for every such
     clause; det(v_i, v_j) = s_i s_j orient(a, b_i, b_j).
   - 0 clauses of any other type; 0 failures of either rule.
   - So **every base clause holds for every real p in general position over every realization of S's labelled order
     type in which S + p has no 7-gon.** G depends only on the signs and is exact for real points.
6. **(b) Added clauses and final CNFs.**
   - All 5,193 added clauses of the 21-point set are 3-literal empty patterns (Motzkin), and their comments match.
   - The same holds for 10,201 / 6,442 / 3,190 added clauses of the 24-point sets, which also contain some 2-literal
     clauses.
   - Each final CNF equals its base followed by its added clauses.
   - Control: each 21/24-point base alone is SAT (CaDiCaL, model checked against every base clause). So these four sets
     are abstractly extendable, and their saturation rests on the coordinate-specific added clauses, as the claim says.
7. **Certificates** (unit `esr-agv-vs-satg7cake`, cake_lpr heap 200, `V/cake/cake.jsonl`).
   - Each run has exactly one line `s VERIFIED UNSAT`; CNF and LRAT hashes equal the claimant's `certify.jsonl`.
   - 21-point final 5207ce67…/LRAT 47b9d514….
   - 24-point finals 7240f0f5…, bb761447…, 0114d5fb….
   - 26-point **bases alone** 7f42493a…, b8a1247d…, which with check 5 means saturated in every realization.

## Not checked

- `conv_sym.py`'s rounding from Z[ζ5] (provenance only).
- The random-point sanity sampling.
- The literature context: DDSZ Thm 4 gives 28 at n = 7, and whether 21 is new was not checked.

## Files

`V/vs_gclauses2.cpp` (7a026c2b…1aa7), `V/vs_g_ctl2.py` (1680ca04…e5f), `V/vs_satcheck.py` (8b6fa768…072c),
`V/vs_ot_invariant.py` (373b848c…0253), `V/cake_all.sh` (7ffe1854…501c), outputs `V/satcheck.out` (c497b56b…0b),
`V/ot_invariant.out` (b10dd0b5…de), `V/cake/cake.jsonl` (140d6984…b117).
