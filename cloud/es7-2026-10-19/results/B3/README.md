# Task B3: (7,5,7)@27 by lookahead cube-and-conquer (20 Oct 2026, 00:36–04:20 UTC)

Instance: 27 x-sorted points (a signotope), no 5-cap, no 7-cup, no convex 7-gon. In
`controls.py` notation this is (k, a, u) = (7, 5, 7), N = 27. The conjectured maximum is
f(7,5,7) = 26, so the instance is conjectured UNSAT.

**Status: OPEN.** Nothing was decided. No model was found, so there is no counterexample, and
no UNSAT claim is made. What this run produced is a cost estimate for a proper Heule-style
cube-and-conquer: roughly **2–3 × 10^5 core-hours**. That needs a cluster; a laptop is out of
the question.

## Where it ran

One cloud container (`env.txt`): 4 cores, 15 GB RAM, Linux 6.18. Tools were built from
source in the session:

| Tool | Version / commit |
|---|---|
| CaDiCaL | 3.0.1 (`c607304`) |
| Kissat | 4.0.4 (`8af8e56`) |
| march_cu, from marijnheule/CnC | `705b60c`, built with `-fcommon` |
| drat-trim / lrat-check | `2e3b2dc` |
| Baek–Balko `etv_signotope` | jcpaik/erdos-szekeres-sat `61bfbd6` |

Scripts are in `scripts/`. Controls reuse `results/B/scripts/controls.py`, `bb_emit.py`,
`lexx.py`, `sigcheckB.c` and `glue.py` unchanged.

## Controls: all pass, both encoders agree (`logs/ctl.json`)

Every SAT model was brute-force checked with `sigcheckB`.

| Instance | Expected | ours (gen_etv.py) | Baek–Balko |
|---|---|---|---|
| (7,4,7)@16 | SAT | SAT 0.03 s | SAT 0.02 s |
| (7,4,7)@17 | UNSAT | UNSAT 1.4 s | UNSAT 1.1 s |
| (7,5,7)@26 (positive control) | SAT | SAT 0.23 s | SAT 0.18 s |
| (6,5,6)@16 = ES(6) | UNSAT | UNSAT 128 s | UNSAT 114 s |

All times are plain CaDiCaL 3.0.1 without symmetry breaking.

Two pipeline checks also ran:

- **Glue control** (`logs/glue_controls.txt`): both 26-point models glue to a 32-element
  signotope (a 6-cap placed deep below) with no convex 7-gon, brute-force checked.
- **Realizer calibration** (`logs/realizer_control_k7a5u7N26.jsonl`): `tools/realizer`
  (installed numpy, scipy and highspy) did **not** realize our 26-point control model in
  120 CPU-s (insertion placed 15 points; best LP slack 0.28). A "not realized" verdict from
  this pipeline therefore carries little weight.

## Cube-and-conquer set-up

- **CNF**: Baek–Balko encoding of (7,5,7)@27 plus the x-reflection lex-leader (`lexx.py`).
  This is `bbx.cnf`: 20,963 variables, 221,918 clauses, 2,925 orientation variables. The CNF
  itself is not committed.
- **Top level**: `march_cu -d 14` on the whole CNF.
  - It took about 33 min and produced 16,365 cubes (19 leaves were refuted by lookahead).
  - For comparison, `-d 8` took 7.7 s for 256 cubes and `-d 11` took 152 s for 2,048 cubes.
  - **Cover check**: CNF ∧ ¬(all 16,365 cubes) is UNSAT, with an LRAT proof that lrat-check
    reports `c VERIFIED` (`logs/cover_d14_lrat_check.txt`). So the top-level cubes cover the
    whole search space.
- **Direct cube probes are far too hard**: every sampled cube at depths 8, 11 and 14 (2, 1
  and 2 cubes) hit the 120 s or 600 s limit unsolved (`logs/probe_*`).
- **Second level** (`scripts/twolevel.py`): for a uniformly random top cube, run
  `march_cu -d 10` on CNF + cube units (91–232 s, about 1,020 sub-cubes each). Then solve a
  uniform random sample of 30 sub-cubes in **one incremental CaDiCaL instance**
  (`scripts/iworker.cpp`: assumptions, learned clauses kept), with a 300 s cap per sub-cube.
- **Allocation**: 3 cores ran the two-level sampler; 1 core ran the Kissat baseline and then
  the third-level tests.

## Cube statistics (`logs/tl2/`, `logs/partial/`, `logs/subcube_time_distribution.json`)

**Top cubes sampled**: 9 to completion of their 30-sub-cube sample (`logs/tl2/top.jsonl`), plus
5 partially. The partial ones are the first 3 top cubes, run before the sampler existed, and
2 in progress at the stop.

**Second-level cubes solved**: 388.

| Result | Count |
|---|---|
| UNSAT | 339 |
| SAT | 0 |
| Timeout at 300 s | 49 |
| Timeout at 600 s | 1 |

**Solve-time distribution** (incremental CaDiCaL):

| Percentile | Time |
|---|---|
| p25 | 1.8 s |
| p50 | 8.9 s |
| p75 | 50 s |
| p90 | ≥ 300 s (timeout) |

- Histogram: under 1 s: 78; 1–10 s: 122; 10–60 s: 103; 60–300 s: 35; timeout: 50.
- 86% of the time goes to cubes over 60 s. The tail decides the cost.
- Top cubes differ a lot in difficulty. Estimated cost per top cube ranges from 7.3e3 s to
  7.1e4 s for the completed samples. In two top cubes (5875 and 9443) most sampled sub-cubes
  timed out: 17 of 24 and 12 of 15.

**Fresh solve vs incremental** (`logs/scratch_vs_incremental.jsonl`): the tail is real.

| Sub-cube | Incremental | Fresh Kissat | Fresh CaDiCaL |
|---|---|---|---|
| 10422/315 | timeout at 300 s | 399 s | over 400 s |
| 7411/790 | 500 s | 190 s | 269 s |

**Third level** (`logs/lvl3.jsonl`, `march_cu -d 6` on a heavy sub-cube):

| Sub-cube | Before | Third-level result |
|---|---|---|
| 10422/315 | ≥ 300 s incremental, 399 s fresh Kissat | 217 s (64 cubes, max 43 s) |
| 13970/701 | ≥ 300 s | 142 s (49 cubes) |
| 5875/369 | ≥ 300 s | ≥ 1,283 s (1 of 64 cubes still timed out) |
| 9443/369 | ≥ 300 s | ≥ 1,161 s after 43 of 64 cubes (stopped) |

Deeper cubing about halves moderate heavy cubes. The hardest cubes are well above the
300 s cap.

**LRAT spot checks** (`logs/lrat_spot.jsonl`): 13 of 13 sampled second-level cubes were
solved from scratch with `cadical --lrat` and checked with lrat-check, all `VERIFIED`
(proofs of 9–43 MB, check time under 1 s each). Together with the top-level cover check,
these are the only certified statements, and each concerns only that cube of this CNF.

**Kissat baseline** (`logs/kissat_baseline_tail.txt`): plain Kissat 4.0.4 on the whole
`bbx.cnf`, 1 core, ran 8,933 s (2 h 29 min, 28.1 M conflicts) with no answer. I stopped it
then to free the core.

## Projection (`scripts/project.py`)

Estimator: total = N_top × mean over sampled top cubes of
[march_s + n_sub × mean sampled sub-cube time]. N_top = 16,365. The interval is a 95%
bootstrap over top cubes.

| Sample | Top cubes | Projected total | 95% interval |
|---|---|---|---|
| 9 completed samples | 9 | 1.97 × 10^5 core-h | 1.3–2.6 × 10^5 |
| Plus 5 partial top cubes | 14 | 3.4 × 10^5 core-h | 1.9–5.3 × 10^5 |

- The scheme would have about 1.5–1.7 × 10^7 leaf cubes.
- Biases go both ways:
  - Time-outs are counted at 300 s, which biases the estimate **down**. The third-level
    tests show some time-out cubes cost over 1,200 s.
  - Adaptive deeper cubing of heavy cubes would bias it **up**, saving about 2× on moderate
    heavy cubes.
  - The 14-top-cube sample is small and the per-top cost is heavy-tailed.
- Honest range: **10^5 to 10^6 core-hours**, centred near 2–3 × 10^5, which is about 25–40
  core-years.
- Sampling caveat: every top cube with 1,024 sub-cubes used the same seeded permutation, so
  the sampled sub-cube indices coincide across top cubes. Each per-top sample is still
  uniform; the variance is somewhat understated.

## Models

None. No cube, at any level, returned SAT, so there was nothing to brute-force check, glue
into a 33-element signotope, or realize. The glue → sigcheck → realizer pipeline was
exercised only on the 26-point control models (above).

## Assessment: laptop or cluster?

**Cluster, and a large allocation.**

- **Laptop**: 2–3 × 10^5 core-hours on 8 cores is about 3–4 years.
- **Comparison with known runs**:
  - about 6–10× the Pythagorean triples run (about 35k core-hours);
  - the same order as Schur number five (about 14 CPU-years, roughly 1.2 × 10^5 core-hours);
  - about 100× KPH's 23-point (7,5,7) theorem (1,727 core-hours).
- **What could cut it**:
  - better cube tuning (adaptive per-cube depth instead of fixed 14 + 10, Heule-style
    `-n`/dynamic cutoffs per top cube);
  - the lemma-injection cardinality constraints from `plan/es7_plan.md` #1;
  - stronger symmetry breaking (only x-reflection is used here).

  Each could plausibly give a few × to 10×. Even a 10× gain leaves about 2–3 × 10^4
  core-hours: a modest cluster for days to weeks, still not a laptop.
- **Before such a run**:
  1. Recurse adaptively on heavy cubes.
  2. Measure the lemma speed-up at k = 6.
  3. Re-estimate with 50 or more top cubes and no 300 s censoring.
