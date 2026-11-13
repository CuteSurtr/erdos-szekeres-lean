# Task F2, second session (`results/F2/s2/`): a new pool of realizable heptagon-free 32-point sets

Nothing here is a claim about ES(7). No 33-point candidate was found.

A second F2 session ran at the same time on another cloud VM and writes to `results/F2/`
(its `env.txt`, `scripts/`, `data/`). This session keeps everything under `results/F2/s2/` so the
two do not collide.

## Results

All 14 new 32-point heptagon-free sets are saturated at the abstract level, and so is every one
of the 13 that sat.c could check geometrically. **No candidate for a 33rd point.**

| | count |
|---|---|
| abstract (7,5,7)@26 models: random-phase SAT, brute-force verified | 6,000 (all OK) |
| random SAT models put through the realizer (Arm A, 4 CPU-s each) | 1,855, **0 realized** |
| realized (7,5,7)@26 sets from SAT-guided exact insertion (Arm F) | **14**, pairwise non-isomorphic |
| new 32-point heptagon-free sets (6-cap deep below each 26-set) | **14**, none isomorphic to the 8,537 pool sets |
| abstract one-point extension (33 x-positions each) | **14 / 14 saturated** (all 33 jobs UNSAT, 0 UNKNOWN) |
| geometric saturation (sat.c, every arrangement face) | **13 / 13 tested saturated** (0 free faces of 109,337); 1 set (F22_307) not tested: no realization with coordinates below 2^27 was found for sat.c |

Every number above was re-checked exactly (Python ints) and by brute force.

## 1. Where it ran

- Cloud VM: 4 cores, 15 GB RAM (`env.txt`), from 00:36 to about 04:30 UTC on 20 Oct 2026.
  Wall times below are on this machine, which was loaded with 4–5 processes.
- Python 3.13 with numpy, highspy and python-sat (CaDiCaL 1.9.5 via `cadical195`). CaDiCaL 3.0.1
  was built from GitHub (`ext_solve` links against it). `tools/trackA/sat.c` was built with `gcc -O2`.

## 2. Abstract models and checks

- **CNF.** `tools/etv/gen_etv.py 26 5 7 7` (A=5: no 5-cap, U=7: no 7-cup, K=7: no convex 7-gon),
  with 17,831 variables and 222,991 clauses. X(i,j,k) is true for ccw, which is a cup triple. A
  plain CaDiCaL solve takes 0.3 s.
- **Generator.** `scripts/gen_models.py`. Each solve uses random initial phases on the 2,600
  orientation variables, a fresh solver every 50 models, and 6 random unit assumptions; each
  model is then blocked on all 2,600 orientation variables. This gave 6,000 distinct models in
  698 s, with a mean pairwise Hamming distance of about 1,200 of 2,600 (sample of 40).
- **Brute force.** `scripts/brute26.c` is an independent exhaustive check of:
  - the signotope axiom on every 4-tuple;
  - every 5-subset for a cap and every 7-subset for a cup (checked against a DP);
  - every 7-subset for convex position (built incrementally from the 4-point test).

  Result: **6,000 / 6,000 OK**.
- **Negative controls** (`data/controls/brute26_controls.txt`):
  - 20 models of `gen_etv 26 6 7 7`: all FAIL cap;
  - 20 models of `26 5 8 8`: all FAIL cup;
  - 20 models of `26 5 7 8`: all FAIL kgon under K=7, and all OK under K=8.

## 3. Realization

### Arm A: random models into the validated realizer (`scripts/realize_models.py`)

- Setup: results/F `realize.py`, m = 1, default portfolio `ins-ff,lp`, **4 CPU-s per model**.
- **0 of 1,855 models realized** (7,610 CPU-s; models 0–1854 of the 6,000).
- Fail-first insertion placed at most 9–19 of the 26 points before an empty cell (median 12–13).
- The lowest alternating-LP slack was 0.18 (median 0.41).
- **Comparison with KPH** (32 / 200,000 ≈ 1.6e-4, with Localizer at 15 s per model):
  - At that rate, 1,855 models would give about 0.3 realizations, so 0 is consistent with it.
  - Our 4 CPU-s budget is also weaker. The other F2 session measured 6 of 12 known-realizable
    extremal 26-sets realized at 4 CPU-s.
  - So this arm cannot sharpen KPH's rate. It only shows that random SAT models are far from
    realizable: fewer than 20 of 26 points ever fit.

### Arms B–E (exploratory, superseded; scripts kept)

| arm | method | how far it got |
|---|---|---|
| B (`arm_b.py`) | alternating penalty descent and phase-guided SAT | about 450–850 violated triples; abandoned |
| C (`arm_c.py`) | random multi-scale geometric candidates, left to right, SAT-checked | at most 17 points |
| D (`arm_d.py`) | SAT-proposed pattern plus LP cell, left to right | at most 14 points |
| E (`arm_e.py`) | fail-first in any label order, repair by random-phase re-solve | at most 19 points |

### Arm F: SAT-guided exact insertion (`scripts/arm_f.py`), the source of every set here

**State.**
- A set of exactly placed integer points, labelled by abstract x-order, so placed labels have
  increasing x.
- A full CaDiCaL model M that agrees with the exact orientation of every placed triple.

**Each step.**
1. For every unplaced label q, a HiGHS LP finds the largest-margin point of q's cell under M. The
   cell is fixed by the signs M(a,b,q) and the x-interval between q's placed neighbours.
2. If any cell is nonempty, the label with the smallest positive margin is placed (fail-first).
   With `--jitter` it goes to a random point of the inscribed disc. The point is rounded to
   integers, rescaling all points by 2^16k when needed, and every new orientation is re-checked
   exactly.
3. Otherwise there is a geometric proposal: an L1-slack LP gives a point for q that violates few
   of M's signs. With `--extra-props` there are also randomly weighted L1 points. CaDiCaL (3,000
   conflicts) is asked for a model under the exact orientations of the placed points plus that
   point. If SAT, q is placed and M is replaced.
4. If no proposal is SAT, it backtracks. `--smart-bt` removes the placed labels most often on
   the wrong side of the best proposal.

**Output.** A complete set is an exact realization of a CNF model by construction. Every 26-set is
then independently re-checked by `post26.py` and brute-forced again by `brute26.c` (14 / 14 OK):
- distinct x and no collinear triple, in Python ints;
- recomputed signs equal to the recorded model.

**Runs** (attempt = one restart from 2 random points; data in `data/armF_runs.txt`):

| config | seeds | attempts | found |
|---|---|---|---|
| no targeted backtrack | 11, 12, 13 | 394 | 0 (max 24 of 26 points) |
| `--smart-bt` | 21, 23 | 244 | 0 (max 25) |
| `--smart-bt --extra-props 2 --jitter 0.5 --bt-depth 3 --backtrack 100` | 22, 24, 25 | 1,074 | **14** |

So the final configuration finds about 1 set per 77 attempts, or roughly 1 per 1,500 CPU-s on
this loaded VM.

**Relation to the task's rule "do not come from annealing or the classical construction":**
- No geometric annealing and no classical template are used.
- The points are placed only into cells of SAT models of the ETV CNF.
- But this is realizability-guided generation, not "realize a random SAT model". It searches
  realizable models directly, so its success rate is not comparable with KPH's per-model rate.

**The 14 sets** (`data/run1/sets26.jsonl`, x-sorted integers of up to 46 bits):
- all have longest cap 4, longest cup 6 and largest convex subset 6;
- their 14 canonical forms (relabelling plus reflection, `chiro.canonical_form`) are distinct.

## 4. The 32-point sets (`scripts/build32.py`)

**Construction.** Every S has no 5-cap, so a 6-point cap A is put deep below S (the Proposition in
`plan/es7_plan.md`):
- every point of A is below every line through two points of S;
- every point of S is above every line through two points of A.

Both conditions are checked exactly, doubling the depth D until they hold. A mixed convex subset
is then a cup of A (at most 2 points) plus a cap of S (at most 4), so the set stays heptagon-free.

**Checks on every 32-set.**
- distinct x and general position;
- exact largest convex subset = 6, by `chiro.largest_convex_subset`;
- brute force (`brute26 32 33 33 7`, every 7-subset) on both the exact set and its compressed
  realization: all OK.

**Compression for sat.c.** sat.c needs |coord| < 2^27, so each 32-set's exact chirotope was
re-realized with the results/F realizer (`build32.py`, then `recompress32.py` with more seeds),
and each result was re-checked exactly against the chirotope of the exact set.
13 of the 14 sets compressed (11 directly in `build32.py`; F24_11 and F25_1 in `recompress32.py`). F22_307 did not, within 5 × 60 plus 20 × 120 CPU-s.

**Novelty.** The canonical forms of all 8,537 pool sets (`inputs/distinct_K7*.txt`) are stored as
sha1 digests in `data/pool_canon_sha1.txt.gz`; they fall in 8,537 distinct classes.
- **None of the 14 new 32-sets matches a pool class** (`data/run1/novelty32.txt`).
- Positive control: pool set `S0_w1400`, mapped by an orientation-reversing affine map and
  shuffled, is found again (`data/run1/novelty_control.txt`).

## 5. Saturation (`scripts/saturate32.py`)

**(a) Geometric.** `tools/trackA/sat.c` on the compressed set:
- an exact sweep of every face of the arrangement of the 496 lines;
- the face count is cross-checked with Euler's relation.

Result: every tested set has 109,337 faces, all faces covered, and **0 bad candidates**.

**(b) Abstract.** `results/A/scripts/ext_solve.cpp` (CaDiCaL 3.0.1, `lucky=0`, no conflict limit)
on `tools/trackB/gen_cnf.py 33 7`:
- the x-sorted signotope of the exact set is fixed through assumptions;
- one job per x-position p = 1..33.

Result: **33 / 33 UNSAT for every set**, 0 UNKNOWN.

**Controls** (`data/controls/`):

| set | geometric | abstract |
|---|---|---|
| pool set `NEAR0_drop9` | 109,337 faces, 0 bad | 33 / 33 UNSAT |
| the same set minus point 5 (31 points, against `gen_cnf.py 32 7`) | 153 bad faces | 17 SAT positions |

So both tests detect a free position when one exists.

Per-set results are in `data/run1/sat32.jsonl`.

## 6. Caveats

- Every UNSAT is a CaDiCaL answer on one CNF, with no proof logged. These are "saturated
  abstractly", not certified.
- 14 sets is a small pool, and all 14 came from one generator with one structural signature (cap
  4, cup 6, convex 6). They are new order types, but they may well lie in one region of the space
  too. A wider search (other phases, other sizes, other rungs) is the natural next step.
- Arm A's 0 / 1,855 does not measure the realizability rate of random models with any precision
  (see section 3).

## Files

- `env.txt`: the machine.
- `scripts/`:
  - `gen_models.py`, `brute26.c`, `realize_models.py`: Arm A;
  - `arm_b.py` … `arm_f.py`: the arms;
  - `post26.py`, `build32.py`, `recompress32.py`, `saturate32.py`, `pipeline.sh`: post-processing;
  - `pool_canon.py`: canonical forms of the pool.
- `data/run1/`:
  - `sets26.jsonl`, `sets32.jsonl` (exact points `points_exact`, compressed points `points`);
  - `brute26.txt`, `brute32.txt`, `sat32.jsonl`, `novelty32.txt`;
  - logs.
- `data/armA_summary.json`, `data/armF_runs.txt`: run statistics.
- `data/controls/`: the controls above.
