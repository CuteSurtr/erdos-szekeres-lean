# Task F2: new realizable heptagon-free 32-point sets and their saturation (20 Oct 2026)

**Outcome.** No 33-point heptagon-free set was found, and no SAT answer was returned at 33 points.

What the run produced:
- **8 realized (7,5,7)@26 sets** (26 points; no 5-cap, no 7-cup, no convex 7-gon), with 8 distinct order types.
- From them, **93 new heptagon-free 32-point sets** (93 distinct order types). None is isomorphic to any of the 8,537 pool sets.
- **All 93 are saturated.** The abstract one-point extension is UNSAT at all 33 positions, in two sweep directions.
- For 43 of the 93 sets, a small-coordinate realization was also found, and `sat.c` saturates every one of them.
- The KPH-style pure abstract stream (random SAT models through the realizer) **realized 0 of 3,089 models**.

The UNSAT answers are CaDiCaL answers on specific CNFs. They were not proof-checked: no DRAT or LRAT was run in F2.

## Machine

- This cloud VM: Linux x86_64, 4 vCPUs, 15 GB RAM (`env.txt`).
- Wall time: 00:28–04:10 UTC.
- Python 3.11.17, numpy 2.4.6, highspy 1.15.1.
- CaDiCaL built from GitHub, commit `c6073042`.
- `tools/trackA/sat.c`, `tools/trackB/brute_kgon.c` and `results/A/scripts/ext_solve.cpp` were built unchanged with gcc/g++ `-O2`.

## Conventions

- The CNF is `tools/etv/gen_etv.py 26 5 7 7`, i.e. N A U K: no 5-cap, no 7-cup, no 7-gon. It has 17,831 variables and 222,991 clauses.
- X(i,j,k) is true iff the triple is ccw iff it is a cup triple (critique item 11).
- KPH's instance is "26 points, no 5-cap, no 7-gon". A 7-cup is itself a convex 7-gon, so the instances are the same.

**Deep-below construction (`scripts/build32.py`).**
- A 6-cap T is placed deep below S. By the Lemma in `plan/es7_plan.md`, a convex subset meeting both parts is (cup of T) ∪ (cap of S), so its size is at most 2 + cap(S).
- Hence S needs to be heptagon-free with max cap ≤ 4 in the chosen "up" direction. Its cups do not matter.
- T_i = (x0 + w·i, −M − i²), with i = −3..2.
- M is the smallest value (by bisection) such that both deep-below conditions hold exactly: T is below every line through two points of S, and S is above every line through two points of T.
- The whole 32-point set is then re-checked from scratch (below).

## 1. Model generation and verification

**Stream A (KPH-comparable).**
- `scripts/gen_models.cpp` (CaDiCaL library) produces models of the ETV CNF, with blocking clauses on the 2,600 orientation variables and a fresh seed per batch.
- Phase modes:
  - mode 0: uniform random phases;
  - mode 1: phases from the orientations of a random point set (uniform, multiscale clusters, noisy parabolas, heavy-tailed, or circles).
- 4,703 models were generated and queued, interleaving the two modes. Later batch files were generated but not used.

**Verification of every queued model (`scripts/brute.c`, `scripts/prep_queue.py`).**
- brute.c checks the signotope axiom on all 4-tuples, computes the max cap and max cup by DP, and finds the largest convex subset by exhaustive DFS.
- All 4,703 models: 0 axiom violations, cap 4, cup 6, largest convex subset 6. All are distinct as bit strings.

**Controls for brute.c** (`data/controls_log.txt`):
- On 10 point sets, brute.c agrees with an independent Python DP and with `chiro.largest_convex_subset`.
- Three single bit-flips of a model give 14, 16 and 20 axiom violations.

## 2. Realization

### Stream A: pure abstract models through the validated realizer

- Realizer: `tools/realizer/realize.py`, default m = 1 portfolio `ins-ff,lp`, 4 CPU-s per model (`scripts/realize_batch.py`).
- Calibration at this budget: 6 of 12 x-sorted 26-point subsets of pool sets (known realizable, extremal) were realized.

| models attempted | phase mode 0 | phase mode 1 | realized |
|---|---|---|---|
| 3,089 | 1,545 | 1,544 | **0** |

**Comparison with KPH (critique item 3).**
- KPH report 32 realizable out of 200,000 models, a rate of 1.6×10⁻⁴, using Localizer at 15 s per model.
- At that rate the expected count here is about 0.5, so 0 of 3,089 is consistent with KPH (P ≈ 0.6).
- Our 95% upper bound on the rate is about 1×10⁻³ (3/3,089). It is roughly 2× weaker still, given our 50% calibrated success at 4 CPU-s.

Diagnostics:
- fail-first insertion placed at most 8–18 of the 26 points (median 12);
- the median best LP slack was 0.41.

Data: `data/streamA/`.

### Stream B: model-guided exact growth (`scripts/grow_guided.py`, `scripts/prefix_server.cpp`)

This stream is new in F2. It uses no annealing and no known construction. It starts from one point and grows a set of exact integer points (the "core"). The core sits at positions i_1 < … < i_k of 1..26, with x increasing with position.

1. CaDiCaL returns a model of the ETV CNF in which every core triple is fixed by assumptions; the other phases are random.
2. Under that model, each free position has a cell: its required orientations with all core pairs, plus the x-order, give an exact 2-D LP (the realizer's `_cell_point`). The most constrained non-empty cell gets a point at its Chebyshev centre. The point is rounded after an exact scaling of the core, and every new orientation is re-checked in integers. The model stays a witness, so the core always stays SAT-extendable.
3. When every cell is empty:
   - ask for a new model (6 times);
   - then run an exhaustive face step: every face of the core's line arrangement inside every free x-slot is SAT-tested as the next point, and placed at the face's Chebyshev centre;
   - at 25 points, run an endgame swap: remove one core point, re-place it exhaustively, then test for a 26th;
   - only then drop 1–3 random core points.
4. At 26 points the whole set is fixed by assumptions and SAT. It is then re-checked independently, as described below.

| run (version) | chains | max size reached | 26 reached |
|---|---|---|---|
| `ggrun`: model step only | 41 | ≤ 25 | 0 |
| `ggdfs`: + bounded DFS over faces | 7 | ≤ 23 | 0 |
| `ggw`: + face step at Chebyshev centres | 27 | ≤ 25 (8 chains at 25) | 0 |
| `ggs`: + endgame swap (final version) | 53 | 26 | **8** |

- The final version realized 8 of 53 chains, about 2.6 wall-minutes of one core per chain.
- That is about 1 set per 36 core-minutes, against KPH's 1,193 core-hours for 32 sets.
- Data: `data/growth/`.

**Independent exact check of each 26-set** (`scripts/verify26.py`, `data/verify26.jsonl`):
- general position (Python ints);
- distinct x;
- cap 4 and cup 6 (Python DP);
- `chiro.largest_convex_subset` = 6;
- brute.c on the x-sorted signotope: 0 axiom violations, cap 4, cup 6, largest convex subset 6.

All 8 pass. Coordinates go up to 2^47. The 8 sets have 8 distinct order types (`chiro.canonical_form`).

Files: `data/sets26/*.pts` (one "x y" per line, x-sorted).

## 3. 26 → 32 (`scripts/process26.py`, `data/process26.jsonl`)

- For each S, all 650 combinatorially distinct sweep directions are scanned. Each uses an exact integer similarity (x, y) → (cx − sy, sx + cy).
- Each direction with max cap ≤ 4 gives one 32-point set (S rotated plus a 6-cap deep below).
- Sets are deduplicated by x-sorted signotope.
- Directions with cap ≤ 4, per S: 29, 5, 11, 11, 7, 14, 5, 11. That gives **93 sets**: `data/sets32/<S>_d<k>.pts`, with coordinates of 60–103 bits.

Note: the 93 sets come from only 8 base sets S, so they are 8 families, not 93 independent samples.

**Exact checks of every 32-set** (`scripts/check32.py`, `data/new32_check*.jsonl`): all 93 are
- in general position;
- of exact largest convex subset 6;
- free of convex 7-subsets by `brute_kgon` (all 3,365,856 seven-subsets), with 0 signotope violations.

**Novelty** (`scripts/novelty.py`, `data/novelty_final.json`): canonical forms (relabelling plus reflection) give 93 distinct order types, and none of them equals any of the 8,537 pool sets (8,537 distinct order types).

## 4. Saturation (33rd point)

**(b) Abstract one-point extension** (`ext_solve`, base CNF `tools/trackB/gen_cnf.py 33 7`, as in `results/A`).
- All 33 x-positions were tested for every set:
  - x-sweep: 93 × 33 = 3,069 instances, **all UNSAT**;
  - second sweep, rotated 90°: 3,069 instances, **all UNSAT**.
- No UNKNOWN answers (conflict limit 10⁶).
- So all 93 sets are **abstractly saturated in both directions**. No pseudo-configuration extension exists for either sweep's signotope, and this covers every geometric 33rd point.
- The answers are not DRAT-certified.

**(a) Geometric exact sweep (`tools/trackA/sat.c`).**
- sat.c needs |coordinates| < 2^27. The realizer was therefore run on each 32-set's exact labelled chirotope (`scripts/compress32.py`, 40–150 CPU-s).
- **43 of 93** got a small realization (max |coordinate| 2^18–2^22), accepted only after an exact re-check of all 4,960 triples.
- sat.c on these 43 gives the same result for every set:
  - 109,337 faces, equal to the Euler count;
  - 0 bad candidates, so **all 43 are geometrically saturated**.
- The same 43 realizations are also abstractly saturated (33/33 UNSAT).
- The other 50 sets were not swept geometrically. Their abstract saturation already implies geometric saturation.

Controls (`data/controls_log.txt`):
- sat.c and ext_solve on two pool sets reproduce `results/A` and `results/F`: saturated, 33/33 UNSAT.
- sat.c on a pool set minus one point finds 14 bad candidates (positive control).
- The deep-below lemma prediction lcs = max(lcs(S), 6, cap(S) + 2) matched the exact count on 6 random sets.

## 5. Candidates

None. No free face and no SAT extension was found, so nothing needed triple-checking.

## Caveats

- The 8 base sets come from one generator (model-guided growth). Whether they are isomorphic to sets from the classical recursive construction was not tested, because no classical 26-point (7,5,7) set was at hand. The 32-point sets do differ from every pool set.
- The 93 sets share 8 cores, so the diversity gained is limited to 8 new (7,5,7)@26 order types.
- Stream B is not a realization rate for random models. It realizes sets directly, so its yield (8/53 chains) is not comparable to KPH's 1.6×10⁻⁴.
- No UNSAT answer here is proof-checked.
- Bugs found and fixed during the run, before any reported number:
  - a wrong critical-angle formula in the direction scan, which made it skip the cap-4 directions;
  - a key collision in the first novelty run, which reported 701 pool sets.

## Files

**`scripts/`:**
- `gen_models.cpp`, `brute.c`, `prep_queue.py`, `realize_batch.py`: stream A.
- `sat_server.cpp`, `repair_loop.py`, `grow26.py`: early generator experiments, superseded.
- `prefix_server.cpp`, `grow_guided.py`: stream B.
- `verify26.py`, `build32.py`, `process26.py`, `check32.py`, `compress32.py`, `novelty.py`, `summarize.py`, `pipe.sh`, `smallpipe.sh`, `ctl_brute.py`.

**`data/`:**
- `sets26/`, `sets32/` (`*_small.pts` = sat.c-sized realizations);
- check logs `*.jsonl`;
- `streamA/`, `growth/`, `controls_log.txt`.

**`summary.json`:** all counts above.

No CNF or proof files are committed.
