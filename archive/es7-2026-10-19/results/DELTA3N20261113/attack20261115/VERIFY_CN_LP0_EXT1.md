# VERIFY_CN_LP0_EXT1: verdict on claim cn-lp0-ext1-5blocks (verifier VS, 18 November 2026, 02:28-02:41 KST)

**Verdict: CONFIRMED WITH ONE CORRECTION.**

- **Main statement: CONFIRMED at its label CERTIFIED.** No 1-point extension (18 points, new point z in gap 0-16, none
  right of r) of any of the five real 17-point blocks is (5,7)-valid with a convex 6-set of 4-cap end points, even as an
  abstract signotope.
  - VS wrote its own encoder from the definitions. All **85 of VS's own CNFs** (5 blocks × 17 gaps) are UNSAT, each with
    a CaDiCaL 2.1.3 LRAT proof that cake_lpr accepted with exactly one line `s VERIFIED UNSAT`.
  - CN's own 85 certificates were re-checked as files: hashes and exact lines.
- **(i) CONFIRMED, EXACT** (own code from the integer coordinates). For each of the five blocks:
  - (5,7)-valid: 0 five-caps, 0 convex 7-sets;
  - r lies in 0 of the 2^16 candidate weak Δs;
  - no gon avoids P0.
- **Correction: the parenthetical "(indeed every abstract)" in the "at least 20 points" sentence is false.**
  - VS found an abstract 19-point signotope that contains R7's block `r7real` with the same rightmost point and is an
    LP0(7) counterexample. Every condition was checked exactly from the definitions (check 6).
  - This agrees with D2's record: the `onn` patterns have abstract models (3,276 for `r7real`) and were closed only by
    BFP cuts, which exclude only realizable signs. VB's VERIFY_LP0_7_REAL_2EXT_VB.md check 3 says the same: own base
    alone is SAT.
  - Correct sentence:
    - every **real** LP0(7) counterexample that contains one of the five blocks with the same rightmost point has at
      least 20 points: 17 EXACT (i), 18 CERTIFIED (this claim), 19 CERTIFIED (`lp0-7-real-2ext`, `-onn`, VB CONFIRMED,
      not re-checked here), with Lemma M PROVED (`t4-lemmas`, V2 CONFIRMED). 20 is attained (`lp0-7-false-real`, `-2`,
      `-3`).
    - for **abstract** signotopes the least size is **exactly 19**: at least 19 by (i) and this claim, and 19 is
      attained (EXACT, check 6).

## Definitions used (task text)

- Lexicographic triples a<b<c; '+' = cup = orient > 0.
- k-cap = every triple a cap.
- Convex 4-set {i<j<k<l} ⟺ s(ijk)=s(ijl) and s(ikl)=s(jkl). Convex k-set = every 4-subset convex.
- (5,7)-valid = no 5-cap and no convex 7-set. Gon = convex 6-set.
- Weak Δ = 4-cap-free set meeting every gon. P0 = points ending no 4-cap.
- LP0(7): r is in a weak Δ, or P0 meets every gon.
- Signotope axiom: on every 4-set the signs (abc, abd, acd, bcd) change at most once.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/cn-lp0-ext1/`)

1. **Own encoder** `V/vs_ext.py`, written from the definitions and not from CN's or D2's code.
   - Variables: one per triple of W that meets a new point (true = cup). B's triples are constants from exact integer
     orientations, and the sign string of `r7real` equals the block file's `signs` field.
   - Clause families, each an instance of a definition, with every equivalence written as its full truth table:
     - the signotope axiom on every 4-set through z;
     - no 5-cap on every 5-set through z;
     - cv_Q ⟺ convexity criterion, on every 4-set through z;
     - every 7-set through z has a non-convex 4-subset (7-sets with a non-convex old 4-subset are skipped);
     - y_K → every triple of K is a cap, for every candidate 4-cap K ending at p;
     - E_p → OR y_K (E_p is constant true if B already has a 4-cap ending at p, constant false if there is no
       candidate);
     - h_H → cv_Q and h_H → E_p, for every 6-set H of W, with or without z, whose old 4-subsets are convex;
     - one clause OR h_H.
   - Soundness: a counterexample W satisfies every clause when each variable is given its meaning.
   - The 85 CNFs have 1 to 143 candidate gons each and no empty clause. CaDiCaL needed 41-218 conflicts (VS's encoding
     differs from CN's, so the counts differ).
2. **Controls** (`V/vs_controls.py`; logs `controls_count.log`, `controls_real.log`, `controls_S.log`).
   - **Validity-only model counts** (gon clause removed, models projected on the 136 triple variables) for `r7real` at
     gaps 1, 2, 3, 4, 5, 15: **204, 332, 166, 110, 115, 242**. These equal D2's and CN's counts.
   - **166 real tests, 0 mismatches.** Each W is a real point set and z one of its points. The encoder, given z's real
     signs as assumptions, must be SAT iff an exact brute force from the coordinates finds no 5-cap through z, no convex
     7-set through z, and a convex 6-set of 4-cap end points.
     - The brute force tests convexity with exact point-in-triangle tests, not with the sign criterion.
     - The W's: random subsets (11-20 points) of the three real LP0(7) counterexamples; random integer points added to
       the five blocks; and the three counterexamples themselves with z = 5, 6, 12, 13, 0, 19 (S), z = 5, 6, 12 (S2)
       and z = 5, 6 (S3).
     - Outcomes: 36 SAT (gon present) and 130 UNSAT (79 without a gon, 42 with a 5-cap through z, 9 with a convex
       7-gon through z), all as predicted.
     - No random point added to a block gave a valid 18-point set, so these samples also found no counterexample.
3. **Own certification** (unit `esr-agv-vs-ext1b`, 02:33:12-02:39:32, CPUQuota 15 %, MemoryMax 400M; house
   `certify_cnf.sh`, cake_lpr heap 200 MB, peak RSS about 25 MB in a foreground test).
   - **85/85 CNFs UNSAT**: CaDiCaL exit 20, and each `.cake.out` has exactly one line `s VERIFIED UNSAT` (`grep -cx`).
   - LRATs (at most 24,517 bytes) are kept as zstd in `V/cert/`; the CNFs are kept as zstd in `V/cnf/`.
4. **CN's artefacts, as files.**
   - `ext1_cn.py`, `cnf_SHA256SUMS.txt` and `cert/certify.jsonl` have the claimed SHA-256 values.
   - All 85 CNFs match `cnf_SHA256SUMS.txt`.
   - Each of the 85 `.cake.out` files has exactly one line `s VERIFIED UNSAT`.
   - Every row of `certify.jsonl` names verdict `s VERIFIED UNSAT` at heap 300; its CNF hash equals the file, and its
     LRAT hash equals the decompressed `.lrat.zst`.
   - CN's cake_lpr was not re-run; VS's own CNFs carry the verdict.
5. **(i) Blocks** (`V/vs_blocks.py`, `blocks.log`, exact from coordinates).

   | block | x increasing, general position | 5-caps | convex 7-sets | gons | 4-caps | weak Δs through r | gons avoiding P0 |
   |---|---|---|---|---|---|---|---|
   | r7real | yes | 0 | 0 | 306 | 170 | 0 | 0 |
   | t1it4 | yes | 0 | 0 | 328 | 169 | 0 | 0 |
   | t1it5 | yes | 0 | 0 | 328 | 168 | 0 | 0 |
   | t1it6 | yes | 0 | 0 | 328 | 168 | 0 | 0 |
   | r7it3 | yes | 0 | 0 | 277 | 173 | 0 | 0 |

   - P0 = {0,1,2,3,5,9,10,12,14,15} in every block.
   - The 306 gons of r7real equal D2's control. Block hashes equal the claim's prefixes.
   - **Lemma M step**: a weak Δ D of W gives the weak Δ D ∩ B of B, because every gon of B is a gon of W. So r ∈ D
     would put r in a weak Δ of B. Hence an 18-point W ⊇ B with max W = r is an LP0(7) counterexample iff it is
     (5,7)-valid and has a gon of 4-cap end points, which is exactly what the CNFs encode.
6. **Abstract 19-point counterexample** (`V/vs_abs19.py`; `abs19_r7real_onnoooooooooooooooo.json`, SHA-256
   `fb2bf880ce35a9049712847bbd0b102144889fa1e0d9fc0f4524a6181e1b5468`).
   - Pattern `onnoooooooooooooooo`: two new points in gap 1 of `r7real`, so old points sit at positions 0, 3-18 and
     r = 18. The model is the first model of VS's encoder extended to two new points.
   - The full 19-point sign function was then checked from the definitions, independently of the clauses:
     - the signotope axiom on all 3,876 four-sets;
     - no 5-cap on all 11,628 five-sets;
     - no convex 7-set on all 50,388 seven-sets;
     - 626 gons and 193 four-caps;
     - **r = 18 lies in 0 weak Δs** (all 2^18 sets containing r enumerated);
     - **2 gons consist of 4-cap end points**, e.g. {3,4,6,7,9,13};
     - the 17 old positions carry r7real's exact signs (0 mismatches).

## Files and hashes

- Code (V): `vs_ext.py` 2a7e3e71…5d8, `vs_controls.py` 0eca7117…0ae, `vs_blocks.py` 448520b4…ec7, `vs_abs19.py`
  c9e66b96…a3e, `drive.sh` e32af193…8f0.
- VS CNF hashes: `V/cnf_SHA256SUMS_VS.txt` (SHA-256 1682cace5de7647fa9771a44dee8797732a2b8cff6464a07c2fb1d68234f272f).
- VS certificates: `V/cert/certify.jsonl` (SHA-256 a68d7bf7640f583a57c6216e62df7fba853497948c9ca7d25aeb3d32785af406),
  plus `<b>_g<g>.lrat.zst`, `.cake.out` and `.cadical.log`.

## Not checked

- D2's 19-point claims `lp0-7-real-2ext` and `-onn` (VB CONFIRMED earlier) were cited, not re-run.
- CN's controls (26,435 real 4-sets, pysat agreement) were not re-run; VS's own controls replace them.
- Whether the abstract 19-point model is realizable: it is not needed for the correction. D2's BFP cuts suggest it is
  not.
