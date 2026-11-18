**Verdict: CONFIRMED** (claim `tspm6-real-15`, verifier V2, 15 November 2026, 15:22-15:27 KST). Label EXACT is
correct. **TS±(6) (T4's K2) is false for a real 15-point set.** Every number in the statement was reproduced by two
independent methods of V2's own, and the parenthetical side statements also check out.

# Independent check: a real 15-point counterexample to TS±(6)

**Claim (filed by T1, 15:22).** The integer point set P in `t1/tspm6_real15.json` (SHA-256 `142707d7…6376d`) has
these properties:
- x is strictly increasing and no three points are collinear;
- it has no 5-cap and no convex hexagon;
- r ends a 4-cap (4 four-caps contain r), and l starts a 4-cap (6 contain l);
- U = P − r has no terminal-safe weak Δ, and V = P − l has no initial-safe weak Δ;
- counts: 24 four-caps, 190 convex pentagons in U, 215 in V.

**Definitions** (candidates.md K2 and §0; THEORY_1115PM.md §0), with n = 6:
- weak Δ of W: 4-cap-free and meets every convex pentagon of W;
- terminal-safe in U: every 3-cap a<b<c in A has (b,c) ending a 4-cap of U;
- initial-safe in V: every 3-cap a<b<c in A has (a,b) starting a 4-cap of V;
- cap: orient < 0 for x-sorted a<b<c; k-cap: every triple a cap.

The point set, x-sorted, with r last:
`(-53431258,154848801) (-8555,53602) (-3952,40182) (-3948,-1913) (-1808,39018) (-1804,-1002) (-1762,-1009)
(-1333,52669) (-1305,-9577) (-1298,48874) (13390,5460) (13722,5390) (18444,-4669) (95833,-13033) (53431258,-6584860)`.

## Method (own code from the definitions; T1's tools were read only afterwards)

The script is `/home/jay/research/data/roadmap-20261115/pm1115/v2/tspm6-real-15/check_tspm_real_v2.py`
(`d8abf0d5388a36d4164922b3630914effd6c0231e804a030375bd9d4d170b7c1`), with `v2lib.py` (`7c8b1ee0…`). It runs two
independent methods, both on the integer coordinates only:

- **M1**: integer orientation signs give a chirotope.
  - Caps: every triple has sign −.
  - Convex k-sets: chirotope triangle containment, cross-checked by the cup/cap split test.
  - All 2^14 subsets of U and of V are enumerated with integer bit masks.
- **M2**: literal.
  - Caps: direct integer `orient` on the coordinates.
  - Convex position: an exact integer convex hull (Andrew's monotone chain); k points are convex iff the hull has k
    vertices.
  - P4(U) and S4(V) by direct search over 4-caps.
  - Every subset A is checked one by one in plain Python.

## Results (`main.out.jsonl`, `81d03ee3…`; under 1 s on one thread)

| quantity | claim | M1 | M2 |
|---|---|---|---|
| x strictly increasing, no collinear triple | yes | yes (asserted) | yes (asserted) |
| signotope violations | – | 0 | – |
| 5-caps / convex hexagons | 0 / 0 | 0 / 0 | 0 / 0 |
| 4-caps of P / containing r / containing l | 24 / 4 / 6 | 24 / 4 / 6 | 24 / 4 / 6 |
| U: 4-caps, convex pentagons, weak Δs | – / 190 / – | 20 / 190 / 1,901 | 20 / 190 / 1,901 |
| **U: terminal-safe weak Δs** | **0** | **0** | **0** |
| V: 4-caps, convex pentagons, weak Δs | – / 215 / – | 18 / 215 / 2,327 | 18 / 215 / 2,327 |
| **V: initial-safe weak Δs** | **0** | **0** | **0** |

The file's `signs` field equals the sign string of the coordinates.

So P is (5,6)-valid, both hypotheses of TS±(6) hold, and both conclusions fail. **TS±(6) fails on P.**

Weak D(5,6) is not touched. P itself has 265 convex pentagons and **2,219 weak Δs**: 1,211 contain r and 978 contain
l (M1, exhaustive; `lr_counts.out.json`). So ROOT and LR both hold on P. Only the terminal-safe and initial-safe
refinements fail.

## Controls (`controls.out.jsonl`, `cda45900…`; M1 and M2 agree in every row)

| set | terminal-safe (U) / initial-safe (V) | expected |
|---|---|---|
| mirror image of P (x → −x, `tspm6_real15_mirror.json`) | 0 / 0; U and V counts swap exactly (2,327 ↔ 1,901, 215 ↔ 190) | swap |
| `t1/root6_real15.json` (the claim's positive control) | **0 / 201** | 0 / 201 |
| lattice-hyp real 13 | 0 / 354 (932 weak Δs of U) | 0 / 354 (VERIFY_ATN_MAIN) |
| d6_12 real | 30 / 214 | 30 / 214 (VERIFY_ATN_MAIN) |

## Parenthetical statements (`side_checks_v2.py`, `70a38199…`; output `side.out.json`, `911cfc05…`)

- **P realizes m15_it7.** P's sign string equals `t1/ts15/feasible/m15_it7.json` (SHA-256 `a4974c95…`).
- **m15_it7 extends to a model of T4's CNF** (COMPUTED). With its 455 signs added as units, T4's `ts/tspm6_m15.cnf`
  (`1467209f…`, as stated) is SAT for pysat's CaDiCaL 1.5.3. This is a solver verdict, not an exact check.
- **It is a different model from T3's.** T3's model has 3 identical copies: `t3/models/tspm6_m15.json`,
  `t1/models/tspm6_m15_t3.json` and the first line of `t1/ts15/models.jsonl`, SHA-256 `76d92627…`. It differs from
  m15_it7 in 119 of 455 signs, and it also extends to a model of the CNF (COMPUTED).
- **T3's model has no x-sorted realization** (EXACT).
  - The certificate is the first line of `t1/ts15/models.jsonl` (CEGAR iteration 1): points [0,2,5,6,8,9,11,12,14] + V,
    76 inequalities.
  - I rebuilt the sub-signature from T3's own sign string, with `+` on (a,b,V). It equals the line's `subsig`, and the
    9-point restriction is a signotope.
  - V2's validated BFP checker (`bfp_v2core.py`, `645ccfab…`, from VERIFY_ROOT6_M15_NONREAL.md) **accepts** the
    certificate: positive integer multipliers up to 164, all totals 0.
  - Negative controls, all rejected:
    - drop item 0;
    - flip a bracket the certificate uses;
    - apply the same certificate to the same 9 points of the real set P, which must fail because P is realizable.

## Comparison with T1's checker (read after my check)

`t1/tools/indep_ts_coords.py` (`86d705f4…`) implements the same definitions:
- hull-size convexity;
- all-triples caps;
- P4(U) and S4(V) from 4-caps of U and V;
- bit-mask enumeration.

It is close to my M2. My M1 is chirotope-based and independent of it. All counts agree.

## Consequence (reading only)

- TS±(6) is CERTIFIED for |S| ≤ 14: claim tspm6-le13 (V3 CONFIRMED) and claim tspm6-14. V2 left tspm6-14 NOT CONFIRMED
  only because its cake_lpr budget was too small; the main session has since re-run that proof
  (MAINSESSION_1115PM.md). [superseded 15 Nov pm (C1 issue 4; note by H1, not by this verifier): V2 changed tspm6-14
  to CONFIRMED at 16:53:54 after checking that re-run; the verdict file keeps the earlier NOT CONFIRMED in its
  `previous` field]
- No valid 16-point set exists.
- So **TS±(6) holds exactly up to 14 points and fails at 15 for real point sets.** LR(6), which TS± implies, still
  holds on P: 978 weak Δs contain l and 1,211 contain r. This is consistent with LR(6) being CERTIFIED for all sizes
  (claims lrr6-certified, lr6-m15-second).

## Files

- Folder: `/home/jay/research/data/roadmap-20261115/pm1115/v2/tspm6-real-15/`, holding the scripts and outputs above.
- Rerun:
  `python check_tspm_real_v2.py /home/jay/research/data/roadmap-20261115/pm1115/t1/tspm6_real15.json`
