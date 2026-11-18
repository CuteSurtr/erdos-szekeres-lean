# VERIFY_D1_C1SIX: verdict on claim d1-c1six (verifier VB, 15 November 2026, 19:34 KST)

**Verdict: CONFIRMED. C1(6) at 15 points is CERTIFIED** (fresh cake_lpr run by VB: exactly one line
`s VERIFIED UNSAT`; CNF, `.zst` and decompressed-stream hashes and the byte count equal the claim). The CNF is exactly
the regenerated ROOT(6)-failure base plus VB's own "r ends a 5-cup" block, and VB read the base encoder line by line
and finds the soundness direction (UNSAT ⇒ no counterexample) correct. The ≤ 14 and ≥ 16 parts rest on proofs that
VB re-ran with cake_lpr tonight (VERIFY_RERUNS_1115EV.md). The consequence for LR(6) at 15 is a valid combination of
CONFIRMED claims.

## Claim (D1, filed 19:28-19:30)

C1(6): in every (5,6)-valid signotope whose rightmost point r ends a 4-cap and a 5-cup, r lies in a weak Δ (4-cap-free,
meeting every convex pentagon). At 15 points by one UNSAT CNF (`d1ev/cnf/c1_rcup6_m15.cnf` = `t3/tools/root_compact.py
6 15` + `p1/addcup.py rcup`); ≤ 14 by ROOT(6) CERTIFIED; ≥ 16 vacuous (claim root6-m16-vacuous). Consequence: with C2(6)
(claim p1-c2six) and Proposition R (claim p1-cupext), LR(6) at 15 points follows a third time. Label claimed: CERTIFIED at
15 points; the other sizes by citation.

## Checks (work dir V = `/home/jay/research/data/roadmap-20261115/pm1115/vb/claims/d1-c1six/`)

1. **Fresh cake_lpr** (unit `esr-agv-vb-cake-d1c1six`, 19:29:37-19:33:13, CPUQuota 95 %, MemoryMax 2700M; own wrapper
   `vb/bin/recake_vb.sh`, LRAT streamed from the kept `.zst` through a FIFO, heap 2000 MB): stdout is exactly the one
   line `s VERIFIED UNSAT`; CNF SHA-256 `078f207ec1e43d6764ae18ddf81a2843d82d4f028b82244204e506bb2b1041ea`, `.zst`
   SHA-256 `9a1c9eba4121f3c8b10d91429e8e91632f9b1a5cf3d219cab60f6974633620f4`, stream SHA-256
   `fb3b99391e6d228c9a0a0395924db06e27db03ee1ba38342192b41095489f4e0`, 5,559,430,678 bytes: all equal the claim.
   Max RSS 2,010 MB, 216 s. D1's CaDiCaL log: `c Version 2.1.3`, `s UNSATISFIABLE`.
2. **CNF composition** (`V/cnfcheck.py`, own): `root_compact.py 6 15` regenerates SHA-256 `152d8a20…` (`p cnf 33542
   86858`), and these 86,858 clauses are the first clauses of the file, in order. The remaining 10,011 clauses equal
   exactly VB's own block written from the definition (for each 4-subset T of {0,…,13} in lexicographic order a fresh
   y_T with (¬y_T ∨ x_t) for the 10 triples t of T ∪ {14}, then ∨_T y_T; x_t = 1 + lexicographic index of t, true =
   cup). Header `p cnf 34543 96869` = expected. Output `V/cnfcheck.out`: ALL_OK.
3. **Base encoder read line by line** (`t3/tools/root_compact.py`, 89 lines, SHA-256 `521f96c4…`, non-`--env` mode).
   For a counterexample S (valid, r ends a 4-cap, r in no weak Δ) set every variable to its defining condition: x_t =
   [t is a cup]; cv_Q = [Q convex]; B(X) = [X ⊆ U contains a gon of U]; Bad(D) = [D + r contains a 4-cap]; F_K = [K is a
   4-cap]. Then every clause holds:
   - signotope clauses forbid the patterns +−+ and −+− in every subsequence of (s(abc), s(abd), s(acd), s(bcd)), i.e.
     they say "at most one sign change";
   - "some consecutive triple of every 5-set is a cup" holds because in a signotope consecutive caps abc, bcd force
     abd and acd to be caps (monotonicity), so a 5-set whose consecutive triples are caps is a 5-cap;
   - cv_Q ↔ (χ(abc) = χ(abd) ∧ χ(acd) = χ(bcd)) is the definition of a convex 4-set; "no convex 6-set" holds;
   - B(X), |X| = 5, implies X convex; for |X| ≥ 6, a gon G ⊆ X misses one of the 6 smallest points of X, so B(X − v)
     holds for that v;
   - Bad(abc) ⇒ abc and bcr caps (true when abcr is a 4-cap); F_K ⇒ abc, bcd caps; Bad(D), |D| = 4: a 4-cap in D + r
     is D itself (F_D) or three points of D plus r (Bad(D − v)); |D| ≥ 5: a 4-cap K misses one of the 5 smallest points
     of D;
   - hypothesis ∨ Bad(abc): r ends a 4-cap;
   - rows Bad(D) ∨ B(U − D) for |D| ≤ |U| − 4 (absent literals dropped): "D is not a rooted Δ". A rooted Δ (weak Δ A of
     U with A + r 4-cap-free) is the same as a weak Δ of S through r (A + r meets the gons through r at r and the others
     at A; conversely Δ − r meets every gon of U), so a counterexample violates no row; for |D| ≤ 2 the literal Bad(D)
     is absent and D + r has ≤ 3 points, for |D| = |U| − 4 = 10 the literal B(U − D) is absent and U − D has 4 points,
     so it contains no gon: in both cases the remaining literal is forced and true.
   So the base is satisfiable by every counterexample; the add-on is satisfied by setting y_T = 1 for the T with
   T ∪ {r} a 5-cup. Hence UNSAT of the file ⇒ C1(6) at 15 points.
4. **Semantic control** (`V/control.py`, own code; pysat used only as a control oracle): the 22 real 15-point ROOT(6)
   failure sets of claim root6-real-15 (`t1/root6_real15.json` and `t1/real/m15_it*_real.json`), exact integer
   orientations: all 22 are (5,6)-valid, r ends a 4-cap, r lies in no weak Δ (0 rooted Δs, exhaustive over 2^14), and
   **r ends no 5-cup in all 22** (consistent with C1(6)). With the 455 triple variables fixed to each set's signs, the
   base CNF is SAT in 22 of 22 (soundness direction on real counterexamples to ROOT(6)) and the full C1 CNF is UNSAT in
   22 of 22. Output `V/control.out`.
5. **Other sizes.** ≤ 14: ROOT(6) is CERTIFIED for 7 ≤ m ≤ 14 (ROOT6_MAIN.md; VB re-ran all eight proofs with cake_lpr
   tonight, VERIFY_RERUNS_1115EV.md) and PROVED for |S| ≤ 2n − 3 = 9 (THEORY_1115PM.md §1.4); ROOT(6) at m is stronger
   than C1(6) at m. ≥ 16: no (5,6)-valid signotope exists (base(5,6,16) UNSAT, two kept proofs, both accepted by
   cake_lpr in VB's re-runs tonight). Point sets give signotopes, so C1(6) holds for point sets too.
6. **Consequence (checked as an argument, hypothesised form: r ends a 4-cap, l starts a 4-cap, |S| = 15).** If r lies
   in a weak Δ, done. Otherwise C2(6) (claim p1-c2six) gives a 5-cup starting at l. The mirror μ (i ↦ 14 − i,
   (i,j,k) ↦ (14−k, 14−j, 14−i), same sign) maps S to a (5,6)-valid signotope (it reverses the sequence of each 4-set,
   so the signotope axiom and the convexity condition are kept) whose rightmost point μ(l) ends a 4-cap and a 5-cup;
   C1(6) at 15 (this claim) puts μ(l) in a weak Δ of μS, so l lies in a weak Δ of S. So LR(6) at 15 follows from C1(6)
   and C2(6) at the same size, as Proposition R (claim p1-cupext, CONFIRMED by V2) states. LR(6) at 15 was already
   CERTIFIED twice (claims lrr6-certified, lr6-m15-second); this is a third route, as the claim says.

## Not done

- D1's own control (`d1ev/tools/ctl_cup.py`, `runs/ctl_cup_n6m15.jsonl`, 25 sets × 2 sides) was not re-run; VB's own
  control above replaces it for the soundness direction.
- `p1/addcup.py` was not used; the add-on was compared against VB's own block (equal).

## Files (V as above)

| file | SHA-256 |
|---|---|
| `V/cnfcheck.py` | `6882b3e40eeccc686348c76d2abe002840d0c94a7a00a41c95fd9f4009ee5c3e` |
| `V/cnfcheck.out` | `d8488bbc5d1abb70798c1b08517c43b348840f010548e9e352a138b4722dbdfd` |
| `V/control.py` | `bc2c8299761920e0423970efba3b3b86fde21e62a490da38f0180ff57e89cd82` |
| `V/control.out` | `2451d590451347241b2400d00bd3fed2dfe3720c95615affb978ef517866dca2` |
| `V/base_root_compact_6_15.cnf` (regenerated) | `152d8a20fe125b975b2d914def64beb9fa16f8e3549a33aef5e8f0e9d67f0f6c` |
| `V/cake/rerun.jsonl` | `a123121ce4bd75552137d3a0643a88805734bf9d527068495ac62afc1d0f9f4e` |
| `V/cake/c1_rcup6_m15.cake.out` (17 bytes, `s VERIFIED UNSAT\n`) | `c680d3bd38a04c7beee7d54999f8f00b43051f75a53cf2bd170ae0cc5f99eb5f` |

No proof was produced, moved or deleted; D1's files were only read.
