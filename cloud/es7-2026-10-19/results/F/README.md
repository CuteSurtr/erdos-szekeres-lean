# Task F: a calibrated realizer for abstract order types (19 Oct 2026)

Nothing here is a claim about ES(7).

- "Realized" means integer coordinates were found and every one of the C(n,3) orientations was
  re-checked in exact arithmetic (Python `int`/`Fraction`) against the model, with no collinear
  triple.
- "Not realized" means only that the heuristic failed within its budget. It does not prove
  non-realizability.

## Summary

| test | result | published / target |
|---|---|---|
| (a) known-realizable chirotopes, final default portfolio, 30 CPU-s | **193 / 200** (100% on 7 of 9 families; scrambled extremal heptagon-free 32-sets 26/30, rising to 28/30 at 120 CPU-s) | close to 100% |
| (b) 4-fold hexagon-free 16-point models, all 528 (33 classes) | **144 / 528 models, 9 / 33 classes** | 18 / 66 solutions, 9 up to isomorphism |
| (b) 5-fold hexagon-free 16-point models, all 2796 (466 classes) | **294 / 2796 models, 49 / 466 classes**, i.e. 98 / 932 solutions | 92 / 948 (also stated as 932), 46 up to isomorphism |
| two-fold heptagon-free 32-point models (40 + 5, 44 classes) | **0 / 45 realized** | (unknown) |
| exact one-point saturation of realized 32-point sets | not run: no set to test | |

On the 16-point symmetric models the realizer reproduces the published 4-fold count exactly. On
the 5-fold models it finds 3 more realizable classes than published.

The old local realizers' 0/30 + 0/30 had two causes:

- **4-fold:** a convention bug, explained in section 5.
- **5-fold:** a sampling artefact. The 30 bundled 5-fold models all lie in classes that are not
  realized here either.

## 1. Machine and budgets

- Local 15-core Apple Mac (`hw.ncpu` = 15: 5 performance + 10 efficiency cores), not a dedicated
  cloud machine. It was shared with other sessions: load average 120 to 130 throughout, and these
  processes ran niced, so each got roughly 0.1 core.
- **All budgets and times are CPU seconds of the realizer process** (`time.process_time`). Wall
  time was 8 to 10 times larger.
- Python 3.14.7, numpy 2.5.3 and highspy 1.15.1 (HiGHS, single-threaded), from the existing
  `.cache/solver-venv`. Nothing new was downloaded.
- The existing CaDiCaL build (`.cache/cadical`) ran `tools/symmetric/enum_models.cpp`.
  `tools/trackA/sat.c` was built with `cc -O2` (macOS needed `-isysroot .../MacOSX26.5.sdk`).

## 2. The realizer (`realizer/realize.py`)

**Input.** A chirotope on n points (all C(n,3) triples), optionally with an m-fold rotational
symmetry in the `tools/symmetric/symcnf.py` convention:
- point o*m + r is R^r q_o, and the centre, if any, is the last point;
- for m >= 3 the direction of R is read from the model (chi(0,1,2) = +1 means counter-clockwise).

**Methods.** They run as a portfolio in three passes (10%, 30% and 60% of the budget, each split
evenly over the methods; every call restarts from scratch):

| method | what it does |
|---|---|
| `sym` | Symmetric penalty descent: only the orbit representatives move, in log-polar coordinates (orbit 0 fixes rotation and scale). Loss = sum over triples of max(0, delta - g)^2, where g = s*det/(l1*l2) and l1, l2 are the two shortest sides (scale-free, so multi-scale configurations are not penalised). Batched Adam over 48 random multi-scale starts plus perturbations of the best chain (Localizer-style leaderboard restarts). For m = 2 the best chain is then polished by `lp2`. |
| `ins` (m = 2) | Exact insertion of whole orbits. For a new orbit {p, -p}, every required orientation with the placed points, including (a, p, -p), is affine in p. The cell is then a convex polygon (a 3-variable LP), and p goes to its Chebyshev centre. The most constrained orbit is inserted first. An empty cell is repaired by symmetric penalty descent from the current positions, then `lp2`. |
| `ins-ff` | The same, point by point and without symmetry (fail-first order, free repairs). The strongest method on extremal heptagon-free 32-point sets. |
| `lp` | Alternating LP (Koshelev-Koshka linear subreduction plus alternation). An abstract extreme point v is sent to y = +infinity, so the angular order around v becomes the x-order of the other n-1 points. x is initialised from a grid: uniform, exponential with a random base, log-normal gaps, two-sided exponential, the best penalty-descent chain, or sorted x-coordinates of known realizations (`--xgrid-pool`). Then it repeats: fix x and solve an LP in y minimising the total slack of s*det/N_t >= delta; fix y and solve the LP in x with the x-order kept. v is finally placed at (0, L) with L computed exactly. |
| `lp2` (m = 2) | The alternation in symmetric form along random directions. Rotations about the centre keep the symmetry, and with the rotated x_o fixed every orientation is linear in the y_o. |
| `free`, `polish`, `ins-free` | Penalty descent on all 2n coordinates; random-direction LP repair of the best configuration; random-order free insertion. None of these realized anything in calibration that the other methods missed. |

**Exactness.**
- Every floating-point success is rounded to integers at increasing scales (2^10 ... 2^64) and
  all C(n,3) signs are re-checked exactly.
- For m = 2 and m = 4 the orbits are generated by the exact integer rotation, so the integer sets
  are exactly symmetric.
- For m = 5 each point is rounded on its own. The chirotope matches exactly, but the set is only
  approximately symmetric.
- The batch drivers then re-check every success independently with `chiro.verify_exact`
  (Fractions), and `make_summary.py` re-checks every committed point file against its decoded
  model.

**`--methods auto` (the default):**
- m = 1: `ins-ff,lp`;
- m = 2 without a centre: `ins,sym,lp,ins-ff`;
- otherwise: `sym,lp,ins-ff,polish`.

## 3. Usage (for other runs)

```
cd cloud/es7-2026-10-19/results/F/realizer          # needs numpy and highspy
# one chirotope: .sig lines "a b c s" (0-based, all C(n,3) triples, s=+1 counter-clockwise)
python3 realize.py model.sig --time 60 --out model.pts                 # no symmetry
python3 realize.py model.sig --m 2 --time 60 --out model.pts           # 2-fold, symcnf labels
python3 realize.py model.sig --m 5 --center --time 60 --out model.pts  # centre = last point
# a symcnf.py model file (one line of signed triple-orbit literals per model), in parallel;
# --K also computes the exact largest convex subset of each realized set; --dedup runs one
# representative per isomorphism class
python3 run_models.py --models ../../../inputs/enum/n32k7m2.models --P 32 --m 2 \
        --out OUT --time 120 --jobs 8 --K 7
# signotope models of tools/trackB/gen_cnf.py (X(i,j,k) lexicographic, true = ccw); a file of
# one model per line, or a solver output with "v" lines
python3 run_models.py --signotope models.txt --P 33 --out OUT --time 120 --K 7
# exact checks + one-point saturation (tools/trackA/sat.c) of realized K-gon-free sets
python3 saturate.py --sat path/to/sat --K 7 --m 2 OUT/*.pts
```

Outputs:
- `OUT/results.jsonl`: one line per model, with `realized`, `method`, `cpu_seconds`,
  `exact_check`, `largest_convex_subset` and diagnostics such as `best_violations` (fewest violated
  triples in penalty descent), `insertion_max_orbits_placed` and `lp_best_slack`.
- `OUT/summary.json`.
- `OUT/modelN.pts`: integer points in model label order.

From Python:
`from realize import realize; realize(chi, n, m, has_center, budget, seed)` returns a dict with
`realized` and `points`.

## 4. Calibration (a): chirotopes known to be realizable

Each trial draws a point set, computes its exact chirotope and discards the coordinates (for
`pool`, the labels are also shuffled). The realizer then starts from its own random starts.
Families (`realizer/calib_random.py`):

- `uniform`: integer points uniform in a square.
- `multiscale`: points in 2 to 5 clusters with log-uniform radii (down to e^-6).
- `pool`: the 8,537 realizable heptagon-free 32-point sets of `inputs/distinct_K7*.txt`. These are
  extremal and multi-scale, the hardest family.
- `sym`: random m-fold symmetric sets.
- `sympool`: centrally symmetric S ∪ (-S) for a random 16-subset S of a pool set. These are
  extremal-structured 2-fold sets, the closest available control for the 32-point models.

Final default portfolio (`auto`), 30 CPU-s per trial (`data/calib_a/run3_final_default`, and the
symmetric families from `data/calib_a/run1`, which already used the final `auto`):

| family | n | m | methods | realized | CPU s per success (median / max) |
|---|---|---|---|---|---|
| uniform | 16 | 1 | ins-ff,lp | 20 / 20 | 0.07 / 0.16 |
| uniform | 26 | 1 | ins-ff,lp | 20 / 20 | 0.57 / 0.95 |
| uniform | 33 | 1 | ins-ff,lp | 20 / 20 | 5.4 / 7.1 |
| multiscale | 33 | 1 | ins-ff,lp | 20 / 20 | 4.9 / 14.2 |
| pool (heptagon-free 32-sets, labels shuffled) | 32 | 1 | ins-ff,lp | 26 / 30 | 4.9 / 20.3 |
| sym | 16 | 4 | sym,lp,ins-ff,polish | 20 / 20 | 0.14 / 0.21 |
| sym (centre in set) | 16 | 5 | sym,lp,ins-ff,polish | 20 / 20 | 0.10 / 0.20 |
| sym | 32 | 2 | ins,sym,lp,ins-ff | 20 / 20 | 4.9 / 13.6 |
| sympool (S ∪ -S, extremal-structured) | 32 | 2 | ins,sym,lp,ins-ff | 27 / 30 | 3.8 / 13.7 |
| **total** | | | | **193 / 200** | |

With 120 CPU-s per trial (`data/calib_a/run2_explicit`), on the same trials (same seeds):

| family | methods | realized | CPU s per success (median / max) |
|---|---|---|---|
| pool 32 | ins-ff | 28 / 30 | 3.0 / 48.8 |
| sympool 32, m = 2 | ins,sym,lp,ins-ff | 30 / 30 | 1.6 / 52.3 |

Earlier portfolios (30 CPU-s, `data/calib_a/run1` and `run2_explicit`) show what each component
adds:

- With `lp,ins,free,polish` (random-order insertion instead of fail-first), pool 32 dropped to
  14/30 and multiscale 33 to 17/20.
- With `ins-ff,lp,free,polish`, pool 32 reached 21/30. Splitting the budget over four methods
  starves `ins-ff`, which is why the final `auto` for m = 1 is just `ins-ff,lp`.
- `free` and `polish` never produced a success in any calibration run.
- `lp` was the successful method for 4 of the 14 pool successes in run1, two of them within
  0.1 CPU-s of the start. In an early test it realized all 3 sets of a small `A7sv2`
  (classical-construction) sample in under 1 s wall each. It failed on the 4 `p2a` pool sets tried
  with 10 CPU-s, with or without x-grids taken from 2,000 known realizations (`--xgrid-pool`).

So, with the final default, the hardest realizable class (scrambled extremal heptagon-free
32-point sets) is realized 87% of the time in 30 CPU-s and 93% in 120 CPU-s. Every other family is
realized 100% of the time in 30 CPU-s, except sympool at 90%.

## 5. Calibration (b): the 16-point 4-fold and 5-fold hexagon-free models

**Enumeration.** All models of `symcnf.py 16 6 4` and `symcnf.py 16 6 5 --center-in-set` were
enumerated with `enum_models` (CaDiCaL, blocking clauses on the triple-orbit variables). The CNFs
are byte-identical to `.cache/es7/symmetric/cnf/*.cnf`.

- 4-fold: 528 models, EXHAUSTED in 1.4 s.
- 5-fold: 2796 models, EXHAUSTED in 1.8 s.
- The first 30 lines equal the bundled `inputs/enum/*.models`.
- Grouped by `chiro.canonical_form` (relabelling and reflection): 33 and 466 classes.

**Labelling multiplicities.**
- 528 = 8 x 66: the choice of orbit 0 (4 ways) times the mirror image, since `symcnf.py` does not
  break reflection.
- 2796 = 3 x 932.
- So the paper's 66 and 932 solutions count mirror images separately, and its "up to isomorphism"
  merges them, like our classes.

**Results** (final code; one representative per class; realizability is a class invariant):

| | classes realized | models realized | in the paper's counting | paper | CPU s per realized class (median / max) | budget per class |
|---|---|---|---|---|---|---|
| 4-fold | 9 / 33 | 144 / 528 | 18 / 66 | 18 / 66, 9 up to iso. | 0.14 / 1.0 | 20 CPU-s, `sym,lp` |
| 5-fold | 49 / 466 | 294 / 2796 | 98 / 932 | 92 / 948 (932), 46 up to iso. | 0.06 / 0.41 | 4 CPU-s, `sym` |

- Every realized set was re-verified exactly. All have largest convex subset 5, so they are
  hexagon-free as required.
- |coordinates| <= 2^18.
- An earlier revision (budget 20 s wall, `sym` only) realized exactly the same 9 and 49 classes.
- A cross-check with the non-symmetric `lp` method (earlier revision, 8 s wall each) on 12 4-fold
  classes realized all 5 of the sym-realized classes in that sample and none of the other 7.

**Why the old realizers got 0/30 and 0/30** (`tools/symmetric/localizer/localizer.c`, `symrealize.c`):

- **Rotation direction (4-fold).** Both programs always rotate counter-clockwise (`CR[r], SR[r] =
  cos, sin(2*pi*r/m)`). For even m without a centre, `symcnf.py` does not fix the direction:
  264 of the 528 4-fold models are clockwise-labelled (chi(0,1,2) = -1). These cannot be realized
  in that parametrisation. Among the 30 bundled 4-fold models, 10 are realizable here, and 4 of
  those 10 are clockwise-labelled.
- **Sampling (5-fold).** For odd m the centre clauses fix the direction, so this bug does not
  apply. But the 30 bundled 5-fold models are the first 30 found by blocking-clause enumeration,
  and all 30 lie in classes that are not realized here either. The audit's "0/30 has probability
  about 4%" assumed independent samples, but consecutive enumerated models are clustered.

## 6. Application: the two-fold heptagon-free 32-point models

**Models.**
- `inputs/enum/n32k7m2.models` (40) and `n32k7m2_seeds.models` (5) are models of
  `symcnf.py 32 7 2`: 16 orbits {q, -q}, 2480 triple-orbit variables.
- They fall into 44 isomorphism classes; `seeds:model1` is isomorphic to `model1`.
- Every model has an abstract convex hull of 4 points (2 orbits).

**Attempts.**
- Pass 1: `ins,sym,lp,polish`, 60 CPU-s per model.
- Pass 2: `ins-ff,ins`, 90 CPU-s per model.
- Pass 2 adds non-symmetric realization attempts (`ins-ff`), because a symmetric chirotope can be
  realizable without a symmetric realization.

PENDING PASS 2

**Result: 0 of 45 realized.**

Diagnostics (pass 1):
- fewest violated triples in symmetric penalty descent: 98 to 302 of 4960 (median 206);
- symmetric insertion placed at most 8 to 11 of the 16 orbits (median 9) before an unrepairable
  conflict;
- the alternating LP never got its total relative slack below 0.435 (median 0.556).

For comparison, under the same portfolio:
- all 20 random centrally symmetric 32-point sets were realized in at most 13.6 CPU-s;
- 27 of 30 `sympool` sets (centrally symmetric, built from extremal heptagon-free sets) were
  realized in 30 CPU-s, and 30 of 30 in 120 CPU-s (median 1.6 CPU-s);
- symmetric insertion places all 16 orbits of those controls.

So these models fail far more decisively than realizable symmetric 32-point controls. This is
heuristic evidence only; no non-realizability certificate was computed.

**Saturation.** No 32-point model was realized, so there was no set to test. The pipeline is ready:
- `realizer/saturate.py` exact-checks a set: model match, general position, exact largest convex
  subset, central symmetry, and the 2^27 coordinate bound.
- It then runs `sat.c`, which counts arrangement faces where a 33rd point avoids a convex 7-gon.
  The face count is cross-checked against Euler's relation.
- Smoke test on a pool 32-set (`A7sv2 SV31_0`): 109,281 faces, all hit, 0 bad candidates, so that
  set is saturated.

## 7. Files

- `realizer/`
  - `realize.py`: realizer and CLI.
  - `chiro.py`: decoding of symcnf/signotope models, `.sig` I/O, exact verification, canonical
    forms, exact largest convex subset.
  - `run_models.py`: parallel batch driver.
  - `calib_random.py`: calibration (a).
  - `saturate.py`: exact checks plus `sat.c`.
  - `make_summary.py`: builds `summary.json` and re-verifies the committed point files.
- `summary.json`: calibration rates, 16-point results, and per-model outcomes and diagnostics for
  the 45 32-point models.
- `data/enum/n16k6m4.all`, `data/enum/n16k6m5c.all`: the complete enumerations.
- `data/sym16/{m4,m5}/`: per-class results (`results.jsonl`, `summary.json`) and the integer
  realizations `modelN.pts` of the 9 + 49 realized class representatives.
- `data/calib_a/<run>/*.jsonl`: calibration (a), one line per trial plus a summary line.
- `data/m32/{pass1,pass1_seeds,pass2,pass2_seeds}/`: 32-point runs.
- `data/m32/classes32.json`: isomorphism classes and hull sizes of the 45 models.

## 8. Caveats

- Every negative here is heuristic, including all 45 32-point verdicts. The calibration shows the
  realizer is not complete even on known-realizable extremal 32-point sets: 2 of 30 scrambled pool
  sets stayed unrealized at 120 CPU-s.
- Budgets are small (60 + 90 CPU-s per 32-point model) because the machine was shared. KPH used
  15 s per model with Localizer on dedicated cores; we do not know the CPU-time equivalence.
- The 5-fold count (98 / 932) exceeds the published 92. The paper's realizability test is
  heuristic, and its 948 vs 932 counts are inconsistent, so this is not a contradiction. Our
  realizations are exact and can be checked from `data/sym16/m5/*.pts` with
  `chiro.verify_exact` (or `make_summary.py`).
