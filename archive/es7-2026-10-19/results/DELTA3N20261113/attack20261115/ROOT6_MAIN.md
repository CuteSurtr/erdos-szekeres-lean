# ROOT(6) for small sets (main session, 15 November 2026, 09:18-09:30 KST)

## Status

- **ROOT(6) is CERTIFIED for every (5,6)-valid signotope, hence every point set, with |S| ≤ 14.** Sizes m = 7-14 each
  have a CaDiCaL 2.1.3 LRAT accepted by cake_lpr with the exact line. Sizes m ≤ 6 are trivial.
- m = 15 and 16: not run to completion (see the extrapolation below).
- For point sets, ES(6) = 17 (Szekeres–Peters) means a (5,6)-valid set has at most 16 points. So m = 7..16 is the whole
  statement for point sets, and m = 15 and 16 are the open sizes. This record does not claim the same bound for
  abstract signotopes.
- Weak D(5,7) and weak D(5,8) are unaffected. No ES bound changes.

**Statement.** ROOT(n): if S is (5,n)-valid (no 5-cap, no convex n-gon) and its rightmost point r ends a 4-cap, then S − r
has a weak Δ A with A ∪ {r} 4-cap-free. A weak Δ here is 4-cap-free and meets every convex (n−1)-gon of S − r.
This is the rooted form that survives on S19′ (n = 7) and on the three real 13-point CONJ-TS′(6) counterexamples
([VERIFY_ATN_MAIN.md](VERIFY_ATN_MAIN.md)).

**Model and soundness.** The encoder is round 6's, unchanged: `/home/jay/research/data/roadmap-20261115/round6/envroot/root_cnf.py`
(`aef1af7a5f63a7d5…`), run as `root_cnf.py 6 m`. (Corrected 13:30: until then this line gave `927e25b4322d83ba…`, which is the
hash of `round6/atn/realize_sig.py`, not of the encoder. Verifier V3 found the slip.)
- Its written soundness argument is in its docstring and in envroot README §2.2. It holds for general n: a
  counterexample, with every auxiliary variable set to its defining condition, satisfies every clause.
- Round 6 used it at n = 7, with positive controls at m = 11 and 12 and a verifier replay.
- **Positive control at n = 6, written by the main session** (`round6/mainsession/root6_control.py`; output
  `root6/control/control.out`). It used the m = 13 CNF and the three real 13-point sets on which ROOT holds:
  - (a) fix the 286 signs and delete exactly the rows of the rooted A with |A| ≤ 8, computed exactly from the
    coordinates (1,068, 460 and 1,098 rows): **SAT** for all three. So the base clauses and every non-rooted row admit
    the real set; this is the soundness direction on actual instances.
  - (b) keep all rows: **UNSAT** for all three.
  - PASS 3/3.

## Results (`round6/mainsession/root6/`; proofs kept as `cert/root6_m<m>.lrat.zst`; house `certify_cnf.sh`, heap 2000)

| m | vars / clauses (rows) | CNF SHA-256 | LRAT bytes | LRAT SHA-256 | CaDiCaL / cake s | verdict |
|---|---|---|---|---|---|---|
| 7 | 111 / 711 (22) | `94ea6486b8b2cbee…` | 394 | `0af50c932d4430a2…` | 0 / 0 | `s VERIFIED UNSAT` |
| 8 | 217 / 1,514 (64) | `b9404ef00e0d6391…` | 496 | `98106c08404a3dd6…` | 0 / 0 | `s VERIFIED UNSAT` |
| 9 | 392 / 2,922 (163) | `2cc8e9d6d10cfba4…` | 2,471 | `ea72c3f945ccff05…` | 0 / 0 | `s VERIFIED UNSAT` |
| 10 | 666 / 5,255 (382) | `fc89445d91873139…` | 134,186 | `011009062d1587ed…` | 0 / 0 | `s VERIFIED UNSAT` |
| 11 | 1,077 / 8,973 (848) | `5649a71d91893d62…` | 4,260,885 | `93cdc86cac5d4a1f…` | 0 / 0 | `s VERIFIED UNSAT` |
| 12 | 1,672 / 14,753 (1,816) | `17a7fc7fe45739fb…` | 70,613,977 | `b028d0a413079163…` | 6 / 2 | `s VERIFIED UNSAT` |
| 13 | 2,508 / 23,631 (3,797) | `59046c71e984ea1a…` | 547,264,401 | `921c6991a147a694…` | 52 / 14 | `s VERIFIED UNSAT` |
| 14 | 3,653 / 37,273 (7,814) | `242a448eb88dff48…` | 2,945,935,220 | `7ee18f7598f52a99…` | 480 / 79 | `s VERIFIED UNSAT` |

Full hashes are in `root6/cert/certify.jsonl` and `root6/SHA256SUMS.cnf`.

**m = 15 and 16 (HEURISTIC).** From m = 13 to 14 the CaDiCaL time grew about 9-fold (52 s to 480 s), and the LRAT
grew 5-8-fold per step. By extrapolation, m = 15 needs about 75 minutes of CaDiCaL and an LRAT of about 15-25 GB, and
m = 16 about 11 hours and roughly 100 GB. Both runs started at 09:23 and were stopped at 09:24. Their partial LRATs (172 MB and 103 MB, not proofs) were
deleted at once. Next step: m = 15 as one job; m = 16 by cubes.

**Not established here.** No implication from ROOT(6) to weak D(5,6) or to any other statement is claimed. ROOT(6) is
the n = 6 member of the surviving rooted form, and its full certification would settle that form at n = 6 only.

## Update, 15 November 13:12-13:25 KST: m = 15 is SATISFIABLE, so ROOT(6) fails for an abstract 15-point signotope

- **Supersedes** the Status line "m = 15 and 16: not run to completion", the m = 15/16 extrapolation and "Next step: m = 15
  as one job; m = 16 by cubes" above. The CERTIFIED range stays |S| ≤ 14.
- **Run.** `root6/run15.sh` (house `certify_cnf.sh`, unit `esr-agx-root6m15`) on `cnf/root6_m15.cnf`
  (SHA-256 `6bd7e8b9a871519a268e6885f670c22afe76f4a0a4383cb06ea7b975ed891be7`, 5,187 vars, 58,503 clauses, 15,914 rows).
  CaDiCaL 2.1.3 printed `s SATISFIABLE` and exited 10 at 13:12:48 after 26.5 s.
  - Log: `cert15/root6_m15.cadical.log` (SHA-256 `6641f3519e3c6ecc…`; its `v` lines are the model).
  - Model literals: `root15/root6_m15.model.lits` (`116f7ce0b223205a…`).
  - The 10 KB log of the 09:23 run that was stopped was renamed `cert15/root6_m15.cadical.log.stopped-0923`.
- **Main session's own exact check** (`round6/mainsession/root15/root15_own_check.py`, `9b418c20587e19fd…`; output
  `root15_own_check.out.json`). The check is independent of the encoder's clause families. It decodes the 455 triple
  variables and recomputes everything by brute force:
  - 4-caps and 5-caps are computed with the all-triples definition; convexity uses triangle containment through a
    chirotope.
  - Signotope violations: 0. Five-caps: 0. Convex hexagons: 0.
  - Four-caps: 98. The consecutive-triples definition gives the same list.
  - 43 four-caps end at r = 14. U = S − r has 292 convex pentagons.
  - A search of all 2^14 subsets of U finds **0 rooted weak Δs**.
  - **So ROOT(6) is false for this abstract (5,6)-valid signotope with 15 points (EXACT, abstract; main session's
    code only).** Verifier V3 **CONFIRMED** it at 13:26 with its own code ([VERIFY_ROOT6_M15.md](VERIFY_ROOT6_M15.md)). V3 checked:
    - the model satisfies all 58,503 clauses, and the CNF regenerates byte-identically from `root_cnf.py 6 15`;
    - the counts above, plus 709 weak Δs if the condition at r is dropped;
    - as a control, each 14-point subset S − p has 7-39 rooted solutions, as the certified m ≤ 14 result requires.
  - The sign string is `root15/root6_m15.json` (`165b1b7ec1958cd3…`).
- **Realizability: open.** `round6/atn/realize_sig.py` ran seeds 1-6 for 150 s each and found no realization. Every seed
  ended with a best minimum margin of about −1.28e-5 and the same count of 6 violated triples. That tool realized S19′
  and the three 13-point CONJ-TS′(6) models within 60 s. The afternoon agents continue in
  [ROOT6_M15_REALIZE.md](ROOT6_M15_REALIZE.md).
- **For point sets, ROOT(6) is open at 15 and 16 points.** ES(6) = 17 bounds (5,6)-valid point sets by 16 points.

## Update, 13:37-13:40 KST: ROOT(6) is false for a REAL 15-point set (EXACT; main session's check from integer coordinates)

- **Supersedes** "Realizability: open" and "For point sets, ROOT(6) is open at 15 and 16 points" above. For point sets the
  least counterexample size is 15, because sizes ≤ 14 are CERTIFIED for all signotopes.
- **Where the set came from.** Agent T1 ran a final-polynomial CEGAR loop on `root6_m15.cnf`. Iteration 8 gave a new
  model (signs SHA-256 `ac822a4630123e85…`), and `realize_sig.py` (seed 1) realized it; the result was rounded to
  integers. File: `/home/jay/research/data/roadmap-20261115/pm1115/t1/root6_real15.json`
  (SHA-256 `28c72627dbce0438ed4bd36a1bd8904ee2c118087645a94aa9d759b210ce2cf0`). T1 reports 13 further real 15-point
  counterexamples from the same run, in `pm1115/t1/real/`. T1's record is [ROOT6_M15_REALIZE.md](ROOT6_M15_REALIZE.md).
- **The set** (x strictly increasing; r = the last point):
  `[[-2687832, 1227453], [-22199, 9905], [-3542, 3674], [-366, -461], [-336, -120], [-333, 2619], [-154, 2025],
  [-152, -143], [-150, -744], [-24, -491], [608, -552], [954, 1503], [1028, 1599], [23067, 46551], [2687832, -1302339]]`
- **Main session's own check** (`round6/mainsession/root15/root15_real_check.py`, `b5665c2fbc154c99…`; output
  `root15_real_check.out.json`). It uses only the coordinates:
  - integer orientations; no collinear triple;
  - convexity by exact point-in-triangle tests on 4-subsets;
  - caps by the all-triples definition;
  - an exhaustive search over the 2^14 subsets of U.

  Results:
  - The sign string in the file matches the coordinates.
  - **0 five-caps and 0 convex hexagons**, so the set is (5,6)-valid.
  - 86 four-caps, **37 of them contain r**.
  - U has 254 convex pentagons and 992 weak Δs, and **0 rooted weak Δs**.
- **Second-party check: verifier V3 CONFIRMED it at 13:39** ([VERIFY_ROOT6_REAL15.md](VERIFY_ROOT6_REAL15.md)), using only the
  coordinates. V3 found the same counts and a sign string equal to the CEGAR model `m15_it8`, which satisfies all
  58,503 clauses. As a control, each 14-point subset P − p has 13-48 rooted solutions, as the certified m ≤ 14
  result requires.
- **Consequence.** The rooted form ROOT(n) fails for point sets at n = 6. It survived on S19′ and on the three real 13-point
  CONJ-TS′(6) sets, but those were checks of single sets, not certificates. ROOT(7) and the other forms are separate
  questions (see PROBES_1115PM.md and THEORY_1115PM.md). No ES bound changes.

## Correction, 14:20 KST: size 16 is vacuous, so ROOT(6) is completely decided

- Agent T4 pointed out (claim `root6-m16-vacuous`, CONFIRMED by a verifier at 14:19) that **no (5,6)-valid signotope on
  16 points exists**. base(5,6,16) is CERTIFIED UNSAT in DELTA2N20261113 (`cnf_hashes.tsv` line 53), and agent T1
  re-certified it with its own encoder (`pm1115/t1/base16/`). Validity is inherited by subsets, so every size ≥ 16 is
  vacuous.
- The Status line and the m = 15/16 paragraph above ("m = 15 and 16 are the open sizes", "m = 16 by cubes, about 11 h")
  were wrong about m = 16. That run was never needed.
- **ROOT(6) is now completely decided.**
  - It holds for every (5,6)-valid signotope with ≤ 14 points (CERTIFIED).
  - It fails at 15 points: for abstract signotopes (EXACT, confirmed) and for real point sets (EXACT, confirmed).
  - Sizes ≥ 16 are vacuous.
- Related: the left-or-right rooted form LRR(6) holds for every (5,6)-valid signotope (claim `lrr6-certified`,
  CONFIRMED). It rests on a new certificate at m = 15, the ROOT(6) certificates at m ≤ 14, and the vacuity of m ≥ 16.
  See [VERIFY_LRR6.md](VERIFY_LRR6.md) and PROBES_1115PM.md.
