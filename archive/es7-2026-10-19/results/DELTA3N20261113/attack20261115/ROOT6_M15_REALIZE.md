# ROOT(6) at 15 and 16 points: is there a REAL counterexample? Follow-ups LRR(6), ROOT(7), LRR(7), TS±(6) (track T1, 15 November 2026, from 13:22 KST)

## Status (final, 18:22 KST; all T1 units stopped)

- **ROOT(6) is false for a real 15-point set (EXACT; claim `root6-real-15`, verifier V3: CONFIRMED 13:39).**
  - The integer point set is in `/home/jay/research/data/roadmap-20261115/pm1115/t1/root6_real15.json` (SHA-256
    `28c72627…10ce2cf0`).
  - It has x strictly increasing, no three collinear points, no 5-cap and no convex hexagon.
  - Its rightmost point r ends 37 four-caps.
  - U = S − r has 254 convex pentagons and **no** rooted weak Δ (exhaustive over all 2^14 subsets).
  - Two separate T1 programs check this: `t1lib.root_check` (from the sign string) and `indep_coords.py` (from the
    coordinates only, convexity by exact convex hulls). V3 used its own code and a third convexity test (VERIFY_ROOT6_REAL15.md).
- **15 is the exact threshold for real sets.** ROOT(6) is CERTIFIED for |S| ≤ 14 (ROOT6_MAIN.md). At 16 points it is
  vacuous: no (5,6)-valid signotope has 16 points (DELTA2N20261113, base(5,6,16) CERTIFIED UNSAT; claim
  `root6-m16-vacuous` by T4). **T1 re-certified this independently with its own encoder** (`tools/base_cnf.py`):
  CaDiCaL 2.1.3 UNSAT in 333 s, cake_lpr `s VERIFIED UNSAT` (heap 1,150 MB, 29 s), proof kept (§Results, item 6).
- **21 real 15-point counterexamples** (`real/m15_it*_real.json`). They realize the 21 BFP-feasible models of a
  BFP-CEGAR run on `root6_m15.cnf`; the realizer needed under 1 s for each. V3's checker confirms all 21 (not filed
  as separate claims).
- **The main session's own m = 15 model is NOT realizable (EXACT; claim `root6-m15-main-nonrealizable`, verifier V2:
  CONFIRMED 13:51).** A biquadratic final polynomial (BFP) certificate exists for its 15-point chirotope: 288
  three-term Grassmann–Plücker inequalities. Already 8 of its points plus the vertical point at infinity V carry one:
  23 inequalities, all multipliers 1. That explains the realizer's persistent 6 violated triples this morning.
- **LRR(6) survives on all 21 real sets.** LRR(6) is T3's rooted left-or-right disjunction. On every set, l starts 22–26
  four-caps and S − l has 220–268 left-rooted Δs (EXACT, `tools/lrr_coords.py`).
- **LRR(6) holds for every (5,6)-valid signotope, hence every point set (CERTIFIED at 15 points + PROVED combination;
  claim `lrr6-certified`, verifier V1: CONFIRMED 14:23, VERIFY_LRR6.md).**
  - T3's `lrr6_m15.cnf` (`0555d770…b6a1a2`, encoder `lr_cnf.py 6 15`) is UNSAT: CaDiCaL 2.1.3 in 1,225 s. Its LRAT
    (3,619,946,969 bytes, `625dffe5…a02f`) was accepted by cake_lpr with `s VERIFIED UNSAT` (heap 1,150 MB, 123 s).
    Proof: `lrrcert/cert/lrr6_m15.lrat.zst`.
  - |S| ≤ 14 follows from the CERTIFIED ROOT(6) (ROOT at m implies LRR at m). |S| ≥ 16 is vacuous (base(5,6,16)).
  - T1 checked the encoder's soundness argument. Each auxiliary variable only implies its defining condition, and
    each row says "A is not a rooted Δ" on its side. T3's positive control passes 3/3.
  - LRR(6) is the per-set left-or-right rooted form, which T4 calls the best surviving reduction (THEORY_1115PM.md).
- **ROOT(7) is false for real 17-point sets.** R7 filed the first one (`root7-real-17`, CONFIRMED by V1). T1 found a
  second, independent one at the same time (`root7_real17.json`, coordinates ≤ 6,741 in absolute value; claim
  `root7-real-17-t1`, CONFIRMED by V1). Its 169 four-caps include 111 at r; U has 314 convex hexagons and 0 rooted Δs.
  T1's CEGAR on T3's `root7_m17.cnf` produced it in iteration 4. Iterations 4–6 were all BFP-feasible and all
  realized. The unit was stopped at 14:12 because R7 owns this question.
- **LRR(7) holds on the real ROOT(7) sets** (EXACT, `lrr_coords.py -n 7`): T1's it4 and it5 sets have 4,129
  left-rooted Δs each; R7's set has 4,316.
- **TS±(6) (T4's K2) is false for a real 15-point set (EXACT; claim `tspm6-real-15`, verifier V2: CONFIRMED 15:26).**
  [corrected 15 Nov pm (C1 issues 8 and 14): was "15:34"; the verdict file time and its time field are both 15:26:34]
  - The set is `tspm6_real15.json` (`142707d7…376d`). It has 24 four-caps; r ends 4 of them and l starts 6.
  - U has 190 convex pentagons and 0 terminal-safe weak Δs. V = S − l has 215 pentagons and 0 initial-safe weak Δs.
  - Two T1 checks agree: `tspm_check` (signs, initial-safe via the mirror) and `indep_ts_coords.py` (coordinates,
    hulls, direct initial-safe test). Control: on `root6_real15.json` the coordinate check gives 0 terminal-safe and
    201 initial-safe sets.
  - T3's abstract TS±(6) model (`tspm6-m15-abstract`) is itself not x-sorted realizable: 9 points + V carry a
    certificate (76 inequalities). The realizer had stalled on it with 9 violated triples.
  - BFP-CEGAR on T4's `ts/tspm6_m15.cnf` (`1467209f…637b1f`), seeded with T3's model, ran 15:20–15:23. Iterations
    1–6 cut obstructions of 8 + V to 11 + V points. Iteration 7 was BFP-feasible and realized in 1 s; 8 of 14
    iterations realized.
  - K2 had already been withdrawn on the abstract counterexample. LR(6) holds (certified), so weak D(5,6) is unaffected.
    TWO-ENV#(6), K2's replacement, holds at 15 (T3, claim `twoenv6-m15`), so no realizability question arises there.
    [corrected 15 Nov pm (as C1 issue 3): in its hypothesised form, r ends and l starts a 4-cap, which is what the
    claim certifies]
- **LR(7) at 17 points: SAT-mode searches found no model (no conclusion).** Unit `esr-agx-t1-lr7c17` ran 15:23–17:16
  (113 min) with phases from `root7_real17.json`. Unit `-lr7c17b` ran 16:38–17:00 with phases from its mirror. Neither
  found a first model. This proves nothing either way.
- **177 distinct real 15-point ROOT(6) counterexamples (EXACT, T1's coordinate checks; not filed as claims).**
  - The file is `real15_all.jsonl` (`c7c476e9…553e`), one JSON line per set: coordinates, sign-string SHA-256 and
    counts.
  - Source: the 21 first sets plus 11 CEGAR runs with random initial phases, 17:00–18:17 (units `esr-agx-t1-div15`,
    `-coll15`). The sets are deduplicated by sign string.
  - Spread: 66–112 four-caps, 25–57 of them at r, 205–308 convex pentagons in U, 0 rooted Δs in every set.
  - **LRR(6) holds on all 177** (116–635 left-rooted Δs), as the certificate requires. This is a consistency control.
  - Smallest coordinates: `root6_real15_small.json` (`05dd1d22…a122`), every |coordinate| ≤ 924:
    `[[-778,-628],[-610,-505],[-372,-110],[-152,265],[-118,-236],[-117,-313],[-35,-32],[-16,-19],[-11,-78],[-10,129],[13,148],[153,42],[176,329],[229,924],[778,449]]`.
    It has 80 four-caps, 45 at r, 219 pentagons in U and 0 rooted Δs; `indep_coords.py` and `collect15.py` agree.
- **Earlier: LR(7) at 17 points, SAT-mode search with realizability (unit `esr-agx-t1-lr7c17`, since 15:23).** The CNF is
  `lr_cnf_stream.py 7 17`, and the phases come from `root7_real17.json`, whose right side already fails. T4 lists
  this as the next test for K1. A real LR(7) failure would refute K1 at n = 7. No answer here means nothing (HEURISTIC).
- **LRR(7) at 15 points: UNSAT (COMPUTED, not certified).**
  - CaDiCaL 2.1.3 found `lrr7/lrr7_m15.cnf` (`651241db…a7f4`) UNSAT in 7,857 s. The LRAT is 23,709,710,423 bytes
    (`99c38ea8…d32c`), kept as `lrr7/cert15/lrr7_m15.lrat.zst`.
  - **cake_lpr stopped with "CakeML heap space exhausted" at heap 1,150 MB**, the most a 1,500 MB T1 unit allows. So
    there is no verdict.
  - Certifying it needs cake_lpr with a heap of about 4,000 MB or more (owner or main session). With ROOT(7) ≤ 14
    (CERTIFIED), a certificate would give LRR(7) for |S| ≤ 15.
- **LRR(7) at 15 and 16 points: certification runs started 14:16** (units `esr-agx-t1-l7a`, `-l7b`; the m = 16 run
  was stopped at 15:20 after 64 min without a verdict, to free its thread; its partial LRAT
  `lrr7/cert16/lrr7_m16.lrat` (8.8 GB) is not a proof and may be deleted with the owner's OK). The CNFs are
  T3's encoder in T1's streaming copy `tools/lr_cnf_stream.py`, which reproduces T3's `lrr6_m15.cnf` byte for byte.
  ROOT(7) ≤ 14 is CERTIFIED (round 6), so this would extend LRR(7) to |S| ≤ 16. Real (5,7)-valid sets with 26 points
  are known (T3's prefix table in PROBES_1115PM.md), so LRR(7) cannot be completed today.
- **T3's abstract 17-point ROOT(7) model (`root7-m17-abstract`) is NOT x-sorted realizable (EXACT; claim
  `root7-m17-t3-nonrealizable`, CONFIRMED by V1; R7's `root7-m17-nonreal-1` is the same fact, CONFIRMED by V2).** Its 9 points
  6,7,8,9,10,11,13,14,16 plus V carry a BFP certificate (27 inequalities, all multipliers 1). The whole 18-element
  configuration has one with 486 inequalities. Without V no certificate was found. T1's own check reproduces T3's
  counts: 163 four-caps, 109 at r, 205 convex hexagons in U, 0 rooted Δs.
  - A BFP-CEGAR search for a REAL 17-point ROOT(7) counterexample runs on T3's `root7_m17.cnf` (unit
    `esr-agx-t1-r7c17`, since 14:04). It is seeded with T3's model (initial phases and first cut) and realizes every
    BFP-feasible model in-process. [superseded 15 Nov pm: the unit was stopped at 14:12 after it produced the real set
    `root7_real17.json` (ROOT(7) item above; claim `root7-real-17-t1`, CONFIRMED)]

**Correction to the task background.** "Every abstract signotope on ≤ 8 points is realizable" is false for x-sorted
realizations. An 8-point signotope plus V is a 9-element rank-3 chirotope. The 8-point sub-signotope above has no
x-sorted realization (exact certificate, claim filed). Uniform rank-3 chirotopes on ≤ 8 elements are all realizable
(Goodman–Pollack), so the safe statement is "≤ 7 points".

## Statement

ROOT(6) (ROOT6_MAIN.md): if S is (5,6)-valid (no 5-cap, no convex hexagon) and its rightmost point r ends a 4-cap of
S, then U = S − r has a weak Δ A (4-cap-free, meets every convex pentagon of U) with A ∪ {r} 4-cap-free.
ROOT(6) is CERTIFIED for |S| ≤ 14 (ROOT6_MAIN.md). Since ES(6) = 17, real (5,6)-valid sets have ≤ 16 points.
Question of this track: does ROOT(6) fail for a real set of 15 or 16 points? **Answer: yes, at 15; 16 is vacuous.**

## Model and soundness

- **Exact check of a candidate** (`t1lib.root_check`, from the definitions). It checks:
  - the signotope axiom on every 4-tuple;
  - no 5-cap;
  - no convex hexagon (convex = every 4-subset in convex position, via chirotope triangle containment);
  - r ends a 4-cap;
  - no rooted weak Δ, by exhaustive search over all 2^(m−1) subsets A of U.

  `indep_coords.py` repeats the check from integer coordinates, with convexity by Andrew's monotone chain.
- **BFP certificates.**
  - Points are p_i = (1, x_i, y_i) and V = (0, 0, 1). The bracket [ijk] = det(p_i, p_j, p_k) is the orientation for
    points, and [a, b, V] = x_b − x_a > 0 for a < b.
  - Any five vectors of R^3 satisfy [abc][ade] − [abd][ace] + [abe][acd] = 0.
  - In a realization in general position the three terms are nonzero. One term has the sign opposite to the other
    two, so its absolute value is the sum of theirs and strictly larger than each.
  - With L_t = log|[t]| this gives strict inequalities L_p + L_q − L_r − L_s > 0. Positive integer multipliers whose
    weighted sum is the zero form give 0 > 0, so no realization exists.
  - An LP (HiGHS) only proposes a support. The multipliers are recomputed in exact rational arithmetic and checked
    by two programs (FLAYER's `bfp.verify_certificate` and T1's `t1lib.check_cert`).
  - A certificate with V refutes x-sorted realizations. One without V refutes every realization.
- **Cuts** (used only to steer the search; no claim rests on them).
  - A minimal obstruction (a sign pattern on the brackets of a certificate on k points, ± V) is forbidden at every
    k-subset Q of the m points, in four families:
    - (a) order-preserving;
    - (b) vertical mirror (y → −y flips all orientations; V is re-oriented);
    - (c), (d) order-reversing, i.e. horizontal reflection x → −x, with or without the mirror.
  - Example, family (d): if x_S(sorted(Q[k−1−c], Q[k−1−b], Q[k−1−a])) = σ(a,b,c) on all brackets, then the reflected
    points R(q_{k−1−i}) form an x-sorted real set with exactly the certified signs.
  - So a real set never violates a cut (control below).
- **16th point lemma (PROVED).** Let S be a real ROOT(6) counterexample and p a point with x_p < x_r such that S + p
  is still (5,6)-valid. Then S + p is a counterexample too. Proof: a rooted weak Δ A′ of U + p would give
  A = A′ − p, which is a rooted weak Δ of U. A is 4-cap-free with A + r 4-cap-free, since these are subsets. It meets
  every convex pentagon of U, because each is a pentagon of U + p avoiding p. This lemma motivated the 16-point
  extension search; the vacuity result above makes that search moot.

## Method

1. BFP on the main session's model (`tools/bfp_model.py`), then greedy minimization (`t1lib.minimize`).
2. BFP-CEGAR (`tools/cegar.py`, pysat CaDiCaL 1.9.5, incremental) on `root6_m15.cnf`. Each loop:
   - solve, then run the exact check;
   - BFP plus minimization, then cuts;
   - a model with no certificate (3 LP seeds) is saved to `feasible/`, and only that exact model is blocked
     (HEURISTIC block).
3. Realizer `realize_sig.py` (main session's, floats only, exact integer check inside) on every BFP-feasible model
   (`tools/real_driver.py`, 60 s, seed 1). Each hit is rechecked from its coordinates.
4. 16th-point search (`tools/extend16.cpp`, exact `__int128`). Candidates were placed around every vertex of the
   arrangement of lines through pairs of S, plus 2 million random multi-scale points per set.
5. LRR(6) from coordinates (`tools/lrr_coords.py`): the left side is the ROOT test on the reflection x → −x.

## Results

| # | item | result | label | verifier |
|---|---|---|---|---|
| 1 | real 15-point counterexample `root6_real15.json` | ROOT(6) fails: 86 four-caps, 37 contain r, 254 convex pentagons in U, 0 rooted weak Δs | EXACT | **CONFIRMED** (V3) |
| 2 | 20 further real 15-point sets `real/m15_it*_real.json` | all fail ROOT(6) (78–88 four-caps, 29–39 at r, 254 or 262 pentagons in U, 0 rooted weak Δs) | EXACT | checked by V3 as an extra (no claim) |
| 3 | main session's model `root6_m15` (`b99b6999…dfe1`) | not realizable: 15-point BFP certificate (288 ineq.); minimal: points 2,3,4,6,7,8,9,12 + V (23 ineq., multipliers 1); also 9 points without V (19 ineq.) [note 15 Nov pm (C1 issue 16): no file for this V-free 9-point certificate is named in this record, `models/m15_main_sub8V_cert.json` has `certificate_noV_on_these_8 = null`, and the claim and V2's verdict cover only the 15-point and the 8 + V certificates, so this part is unverified] | EXACT | **CONFIRMED** (V2, `root6-m15-main-nonrealizable`; VERIFY_ROOT6_M15_NONREAL.md) |
| 4 | BFP-CEGAR on `root6_m15.cnf`, 32 iterations (13:30–13:38) | 11 models carried certificates (minimal obstructions: 8 + V (3), 9 (2), 9 + V (1), 10 + V (2), 11 (1), 12 (2)); 21 were BFP-feasible, and all 21 realized | EXACT per model | – |
| 5 | 16th point for each of the 21 real sets | none found (about 2.07 M candidates per set). Positive control: with one point removed, the search finds valid replacements. | HEURISTIC (search) | – |
| 6 | base(5,6,16) ("no 16-point signotope without 5-cap and convex hexagon"), T1's own encoder `tools/base_cnf.py` (2,380 vars, 41,496 clauses; CNF `1a556b6e…bff6c`) | UNSAT: CaDiCaL 2.1.3 333 s; LRAT 953,140,079 bytes (`61337761…a5a7`), cake_lpr `s VERIFIED UNSAT` (heap 1,150 MB, 29 s); proof `base16/cert/valid56_m16.lrat.zst` | CERTIFIED (independent re-certification of DELTA2N's base(5,6,16)) | no separate claim (supports T4's `root6-m16-vacuous`) |
| 7 | LRR(6) on the 21 real sets | holds on all: l starts 22–26 four-caps; 220–268 left-rooted Δs | EXACT | – |
| 8 | LRR(6) at 15 points: BFP-CEGAR (pysat) | ran 13:44–14:03 without a first model; stopped to free its thread (see item 12 for the certificate) | – | – |
| 9 | T3's ROOT(7) model `root7_m17_s1` (file `8d6bedc1…efebd`) | not x-sorted realizable: points 6,7,8,9,10,11,13,14,16 + V, 27 ineq. (multipliers 1); 18 elements: 486 ineq.; no certificate without V | EXACT | **CONFIRMED** (V1, `root7-m17-t3-nonrealizable`) [corrected 15 Nov pm (C1 issue 8): was "pending"; verdict file 14:10:27] |
| 10 | BFP-CEGAR on T3's `root7_m17.cnf` (SHA-256 `44626ab2…f154d5`), n = 7, 14:04–14:12 | 8 iterations: obstructions 9 + V (seed), 13 + V, 11 + V (×2), …; iterations 4–6 BFP-feasible and realized in 0.4 s each | EXACT per model | – |
| 11 | real 17-point ROOT(7) counterexample `root7_real17.json` (`d30d09d3…5829`) | ROOT(7) fails: 169 four-caps, 111 at r, 314 convex hexagons in U, 0 rooted weak Δs | EXACT | **CONFIRMED** (V1, `root7-real-17-t1`) |
| 12 | LRR(6) at 15 points (T3's `lrr6_m15.cnf`) | UNSAT, cake_lpr `s VERIFIED UNSAT`; with ROOT(6) ≤ 14 and vacuity ≥ 16: LRR(6) holds for all (5,6)-valid signotopes | CERTIFIED + PROVED | **CONFIRMED** (V1, `lrr6-certified`) |
| 13 | LRR(7) on real ROOT(7) sets | holds: 4,129 / 4,129 / 4,316 left-rooted Δs | EXACT | – |
| 14 | LRR(7) at 15 (`lrr7/lrr7_m15.cnf`, `651241db…a7f4`, 8,125 vars, 129,486 clauses) and at 16 (`lrr7/lrr7_m16.cnf`, `5f04ba2d…572d`, 12,026 vars, 216,967 clauses) | m = 15: **UNSAT** (CaDiCaL 2.1.3, 7,857 s; LRAT 23.7 GB `99c38ea8…d32c`, kept as zstd); cake_lpr: heap exhausted at 1,150 MB, no verdict. m = 16: stopped 15:20 without verdict (4.4 M conflicts) | COMPUTED (m = 15) | – |
| 15 | T3's abstract TS±(6) model (`tspm6-m15-abstract`) | not x-sorted realizable: 9 points + V, 76 ineq. | EXACT | no claim filed (superseded by item 16) |
| 16 | real 15-point TS±(6) counterexample `tspm6_real15.json` (`142707d7…376d`) | TS±(6) fails: 24 four-caps, r_caps 4, l_caps 6, 190 / 215 pentagons in U / V, 0 terminal-safe, 0 initial-safe | EXACT | **CONFIRMED** (V2, `tspm6-real-15`) |
| 18 | 177 distinct real ROOT(6) counterexamples `real15_all.jsonl` | all fail ROOT(6) and satisfy LRR(6); 66–112 four-caps, 25–57 at r, 205–308 pentagons in U | EXACT | no claim |
| 19 | smallest-coordinate real ROOT(6) counterexample `root6_real15_small.json` | max \|coordinate\| 924; 80 / 45 / 219 / 0 | EXACT | no claim (same statement as `root6-real-15`) |
| 17 | LR(7) at 17, SAT-mode BFP-CEGAR (`lr7c17/`; CNF `lrr7_m17.cnf`, 17,466 vars, 361,711 clauses) | stopped 17:16 after 113 min without a first model (second search from mirrored phases: 22 min, none) | no conclusion | – |

CEGAR iterations at m = 15 (`cg15/table.md`):

| iter | model sign-string SHA-256 | 4-caps / at r | pentagons of U | BFP (minimal obstruction) | realizer (60 s, seed 1) |
|---|---|---|---|---|---|
| 1 | `fd96978c44e85610…` | 93 / 38 | 237 | 9 pts, 26 ineq, 62 brackets | – |
| 2 | `c2818792b2ca309c…` | 82 / 58 | 229 | 10 pts + V, 86 ineq, 144 brackets | – |
| 3 | `3be8a54eef5297a8…` | 81 / 57 | 229 | 10 pts + V, 30 ineq, 89 brackets | – |
| 4 | `8498c795a7740d53…` | 77 / 53 | 249 | 9 pts, 21 ineq, 59 brackets | – |
| 5 | `bf5e485c5e245b4c…` | 77 / 53 | 249 | 8 pts + V, 26 ineq, 62 brackets | – |
| 6 | `6a634111eb4a137b…` | 94 / 40 | 240 | 8 pts + V, 50 ineq, 82 brackets | – |
| 7 | `520708bf00c8a4dc…` | 90 / 36 | 252 | 8 pts + V, 32 ineq, 67 brackets | – |
| 8 | `ac822a4630123e85…` | 86 / 37 | 254 | none (BFP-feasible) | REALIZED (= `root6_real15.json`) |
| 9, 10, 12–17, 19, 21–24, 26–32 | see `cg15/table.md` | 78–88 / 29–39 | 254 or 262 | none (BFP-feasible) | all REALIZED in ≤ 0.3 s, exact coordinates OK |
| 11 | `e40bbd8e705c69e1…` | 85 / 36 | 244 | 9 pts + V, 73 ineq, 110 brackets | – |
| 18 | `38427aede7f1b8ae…` | 83 / 34 | 254 | 12 pts, 85 ineq, 175 brackets | – |
| 20 | `470f3a9443aca694…` | 85 / 36 | 254 | 11 pts, 26 ineq, 80 brackets | – |
| 25 | `21d2e8554badecf7…` | 79 / 30 | 254 | 12 pts, 74 ineq, 160 brackets | – |

## Controls

- Each cut is violated by its own model. 300 random real 15-point sets (exact integers) violate none of the cuts from
  the main model's obstructions (`tools/control_cuts.py`).
- `t1lib.root_check` reproduces the main session's counts on its model: 98 four-caps, 43 at r, 292 pentagons, 0.
- `lrr_check` reproduces T3's left-side counts on the same model (26 four-caps start at l, 231 left-rooted Δs). Its
  left side on `m15_it8` equals `lrr_coords.py` from coordinates (25, 227, 258).
- Encoder control for item 6: the real set `root6_real15.json` satisfies all 29,848 clauses of `base_cnf.py 6 15`, with
  every convexity variable set by an exact convex hull test.
- A real 10-point set has no BFP certificate (`t1lib.selftest`). The GP identity holds on random integer points
  (`bfp.selftest`).

## Files (work dir `/home/jay/research/data/roadmap-20261115/pm1115/t1/`)

| file | SHA-256 |
|---|---|
| `root6_real15.json` (coordinates + signs) | `28c72627dbce0438ed4bd36a1bd8904ee2c118087645a94aa9d759b210ce2cf0` |
| `models/m15_main.json` | `165b1b7ec1958cd373aaddd2676c46a0be0e6f835482169fab06295c57d733fe` |
| `models/m15_main_bfp_noV.json` (15-point certificate) | `4d219796e23d927b8f39f8df513ab24f2ffcff542da2b163d0a3b758afad2382` |
| `models/m15_main_sub8V_cert.json` (8 + V certificate) | `9335f5538284cc1b6651c72db3803d3ec018f1525922c42ccfe59b47948c049d` |
| `models/m15_main_bfp_withV.json` (16-element certificate) | `a30f2d03c1d444bd4cb853f2dbda08805784f802a5b49e130abc651ac4618586` |
| `tools/indep_coords.py` | `e4edd44d992add3a9a4d36548448693f8723cb6e09f6c2c6113d76ece3d4253a` |
| `tools/bfp.py` (copy of FLAYER20261113/tools/bfp.py) | `147b3690d8f2080a80cb176433c5808182b6677ef17f5aa49e2e249bf5aea748` |
| `root6_m15.cnf` (main session) | `6bd7e8b9a871519a268e6885f670c22afe76f4a0a4383cb06ea7b975ed891be7` |
| `realize_sig.py` (main session) | `927e25b4322d83badb85fc4dbba2f981f3e212ca627a17f69a4ede00adf04933` |

`tools/indep_coords.py` was generalized at 14:03 to any n (optional second argument; default 6, same output keys
renamed). The version named in claim `root6-real-15` is kept byte-identical as `tools/indep_coords_n6_claim.py`
(`e4edd44d…253a`).

Further tools: `tools/indep_ts_coords.py` (`86d705f4…62bb6`), `tools/lr_cnf_stream.py` (byte-identical output to T3's
`lr_cnf.py` on `lrr6_m15.cnf`).

Other tools: `tools/t1lib.py`, `cegar.py`, `real_driver.py`, `extend16.cpp`, `base_cnf.py`, `lrr_coords.py`,
`control_cuts.py`, `bfp_model.py`, `bfp_robust.py`. Data: `cg15/` (log, models.jsonl, cuts.cnf, feasible/),
`real/` (realizations, `realize_table.jsonl`), `ext16/`, `base16/`, `lrr15/`.

## What remains

- LRR(7) at 15: re-run cake_lpr with heap ≥ 4,000 MB. Unpack with `unzstd lrr7/cert15/lrr7_m15.lrat.zst` (23.7 GB),
  then `cake_lpr --CML_HEAP_SIZE=4500 lrr7/lrr7_m15.cnf lrr7_m15.lrat` and grep the exact line. LRR(7) at 16 is not
  feasible today with one thread.
- LR(7) at 17 and 16: open (searches found no model; nothing proved).
- LP0(7) realizability: R7 is running it (`root7-m17`/`lp0` section of ROOT7_M17_REALIZE.md); T1 did not duplicate it.
  [superseded 15 Nov pm: R7 finished; none of the 108 models has an x-sorted realization (claims `lp0-7-w19-nonreal`,
  `lp0-7-realblock-nonreal`, `lp0-7-scan-all-nonreal`, all CONFIRMED); LP0(7) stays open for point sets]
- A small-coordinate counterexample: done after all. The random-phase runs produced one with every |coordinate| ≤ 924
  (item 19). The earlier SLSQP attempt on `m15_it8` had failed.
- Technical: in pysat 1.9.dev20, `Cadical195.interrupt()` did not stop `solve_limited`. `cegar.py` deadlines therefore
  take effect only between solves, and the unit's RuntimeMaxSec is the real limit. One stuck diversity run was
  terminated by hand at 17:57.
- Housekeeping for the owner: the partial LRAT `lrr7/cert16/lrr7_m16.lrat` (8.8 GB, an interrupted run, not a proof)
  may be deleted with the owner's OK. Every proof (base16, lrr6, lrr7 m = 15) is kept as zstd.

## Resume

```bash
T1=/home/jay/research/data/roadmap-20261115/pm1115/t1; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
$PY $T1/tools/indep_coords.py $T1/root6_real15.json            # exact check from coordinates (~1 s)
$PY $T1/tools/lrr_coords.py $T1/real/m15_it8_real.json         # LRR(6) both sides
# CEGAR (resumes from <out>/cuts.cnf); mode root or lrr
systemd-run --user --unit=esr-agx-t1-cg15 -p CPUQuota=100% -p MemoryMax=1500M -p MemorySwapMax=0 -p RuntimeMaxSec=3600 \
  --nice=10 --working-directory=$T1 $PY -u tools/cegar.py 15 <cnf> $T1/cg15 <deadline_epoch> 1 root
```
