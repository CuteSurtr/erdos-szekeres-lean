# VERIFY_LOWERBOUND_L18_OCT56: verdict on claim lb-l18-oct56-real (verifier VS, 18 November 2026, 02:48-03:00 KST)

**Verdict: CONFIRMED at the claimed labels.**
- (a), (c) and (d) are EXACT by VS's own code.
- (b) is CERTIFIED. cake_lpr, re-run by VS, accepts the claimant's LRAT for d56g_final.cnf.
- **Every clause of that CNF is justified by VS's own exact code, without using l1enc's soundness argument:**
  - 90,914 base clauses are exactly VS's own octagon encoding G;
  - the other 187,992 base clauses and all 4,041 added clauses forbid sign patterns that are geometrically empty for
    S (exact Motzkin test).

So geometric octagon saturation is not an order-type invariant. S is saturated; S′ has the same labelled order type and
the same x-order, and S′ + p is in general position with no convex octagon.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/l18-oct56/`; L = `pm1115/l1118/d56/`)

1. **Files.** The SHA-256 values of `d56_S.txt`, `d56sub_S.txt`, `d56sub_Sp.txt`, `d56_S.cnf`, `d56g_added.txt`,
   `d56g_final.cnf` and the decompressed LRAT equal the claim.
2. **(a) and (d), exact convex counts** (`V/vs_convk.cpp`).
   - Method: C++ with 128-bit orientations. It checks that x is strictly increasing and that the set is in general
     position, then counts the convex m-gons as Σ caps(l,r,c)·cups(l,r,u) with c + u − 2 = m.
   - Control: 150 random sets against an exact point-in-triangle brute force (`V/vs_convk_ctl.py`), 0 mismatches.

   | set | general position | convex m-gons, m = 3..7 | m = 8 | largest |
   |---|---|---|---|---|
   | S (56) | yes, x increasing | 27,720 / 249,544 / 1,174,834 / 2,700,225 / 2,373,304 | 0 | 7 |
   | S′ (56) | yes, x increasing | the same | 0 | 7 |
   | S′ + p (57, sorted by x) | yes | 29,260 / 268,170 / 1,282,326 / 2,974,012 / 2,621,044 | **0** | **7** |

3. **(c) Same order type** (`V/vs_oct56.py`).
   - All 27,720 triples have the same sign in S and S′, and no triple is collinear.
   - Both files are x-sorted in label order.
   - S′ differs from S exactly in points 12-19, the 8 points of D inside block P_3.
4. **(b) CNF structure.** `d56g_final.cnf` is `d56_S.cnf` (278,906 clauses, all with 3 literals over the 1,540
   variables X(a,b), a<b, variable = 1 + lexicographic rank) followed by the 4,041 clauses of `d56g_added.txt`, in
   order. Each added clause's comment lines (a, b, sign) equal its decoded literals.
5. **(b) VS's own encoding G of "S + p has no convex octagon"** (`V/vs_gclauses.cpp`).
   - Since S is octagon-free, an octagon of S + p contains p. It exists iff, for some convex heptagon Q of S (CCW order)
     and some i:
     - p lies beyond the edge q_i q_{i+1};
     - p lies on the inner side of the lines q_{i−1}q_i and q_{i+1}q_{i+2}.
   - Then inserting p between q_i and q_{i+1} keeps all turns left with total turning 2π, and conversely.
   - G has one 3-clause per (Q, i). VS enumerated the 2,373,304 heptagons (equal to check 2's count), giving
     16,613,128 clause instances and **90,914 distinct clauses** (`V/G8.clauses`, d3b867c9…).
   - Controls:
     - 30 small random sets: the polygon counts equal vs_convk's;
     - `V/vs_g_ctl.py`: 200 random real (S, p) with k = 5..7. "X(p) violates G" holds exactly when vs_convk's count of
       k-gons grows when p is added. 181 + 19 cases, **0 mismatches**.
6. **(b) Every clause of the final CNF classified** (`V/vs_base_classify.py`, `base_classify.json`).
   - **90,914 base clauses are clauses of G.** All of G occurs in the base.
   - **187,992 base clauses forbid a geometrically empty pattern.** VS's exact Motzkin test (`motzkin_empty` in
     `vs_oct56.py`) finds λ ≥ 0, λ ≠ 0 with Σλ_i s_i n_i = 0 and Σλ_i s_i c_i ≥ 0 on a subset of the three open
     half-planes s_i·orient(a_i, b_i, p) > 0. This needs exact integers only.
   - **0 base clauses are left unexplained.**
   - **All 4,041 added clauses** (3 literals each) forbid geometrically empty patterns by the same test.
   - So every real p in general position with S + p octagon-free satisfies every clause.
7. **(b) Certificate.** VS ran cake_lpr itself (unit `esr-agv-vs-oct56cake`, `--CML_HEAP_SIZE=290`, MemoryMax 400M,
   peak RSS 300,156 KiB, 1.2 s) on `d56g_final.cnf` (1923fd2a…) and the claimant's LRAT (f373582f…, 54,978 bytes): the
   output has exactly one line, `s VERIFIED UNSAT`. Hence S is geometrically octagon-saturated.
8. **Side observations.**
   - G plus the 4,041 added clauses alone is **SAT** (VS's run, `V/vs_G8_plus_added.cnf`, CaDiCaL exit 10). The
     empty-pattern part of l1enc's base, i.e. its realizability content (for example 3 lines through a common point),
     is needed for UNSAT.
   - Control: S′ + p's sign vector satisfies all of G and all 278,906 base clauses and violates 52 added clauses. This
     is as it must be: those patterns are empty for S's lines but realized for S′'s.

## Not checked

- Rebuilding S and S′ with `build_d56.py` (the builder writes into its working directory). The claim's statements are
  checked on the files themselves, so the provenance of the coordinates does not matter for them.
- The literature statement (DDSZ Thm 4 instance) and the novelty of the observation.

## Files

`V/vs_convk.cpp` (d43c5d0a…f426), `V/vs_convk_ctl.py` (066cd8c9…e836), `V/vs_oct56.py` (7f942cdf…bfd76),
`V/vs_gclauses.cpp` (38f2b191…4c3b), `V/vs_g_ctl.py` (655ddbf6…1dd1), `V/vs_base_classify.py` (7b78ab61…ed2a),
`V/G8.clauses`, `V/base_classify.json` (9b976418…7009), `V/vs_oct56_result.json`, `V/cake290.out`,
`V/vs_G8_plus_added.cnf` (07f9c917…4b5604, SAT).
