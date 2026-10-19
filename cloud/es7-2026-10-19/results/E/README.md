# Task E: symmetric 33-point searches (3-fold and D3), 19 October 2026

Nothing in this directory is a theorem. "UNSAT" below always means "UNSAT of one specific CNF
(encoding X)"; the encodings were tested but are not formally verified.

## Machine

- Apple M5 Pro, 15 cores (5 performance + 10 efficiency), 48 GB RAM. This was the user's
  local machine, not a dedicated cloud box, and it was shared with sibling tasks: the load
  average was about 46 when work started and 90 to 105 for most of the run. So "most cores"
  meant 7 CaDiCaL workers getting a fraction of a core each.
- Memory was the binding limit. A worker on the 3-fold CNF peaks at about 7.2 GB with
  CaDiCaL's default bounded variable elimination and about 3.1 GB with `--elim=0`. All runs
  below use `--elim=0` (`logs/memtest.txt`).
- Tools built from source: CaDiCaL 3.0.1 (git c607304), drat-trim and lrat-check (git
  2e3b2dc). Python 3.14.7. `logs/environment.json` has the details.

## Summary

| Instance | CNF (sha256 prefix) | Status |
|---|---|---|
| D3, 33 = 5×6 + 3, mirror axes through the 3-orbit, K = 7 (`d3cnf.py`) | `n33k7d3` 72ebbae0 | **UNSAT, LRAT-checked** (lrat-check: `c VERIFIED`). Closed at the root cube in about 180 s wall. |
| The same D3 class built a second way: 3-fold CNF plus 1,970 reflection clauses (`c3refl.py`) | `n33k7m3refl` cc329387 | **UNSAT, LRAT-checked** (`c VERIFIED`). The plain solve took 26.9 s CPU; the LRAT solve took 28.1 s CPU and wrote a 650 MB proof. |
| The same D3 class with the direct K-gon encoding: each 7-set clause over its 35 conv₄ flags, no conv₅/conv₆ layer (`d3cnf.py --kgon direct`) | `n33k7d3direct` 7796d999 | **UNSAT, LRAT-checked** (15.9 s CPU, 153 MB proof, `c VERIFIED`). |
| 3-fold, 33 = 11 orbits of 3, auxiliary centre, K = 7 (`symcnf.py 33 7 3`) | `n33k7m3` 4c214b4c | **Open.** Still running when this was committed. A later commit updates this row. |

No model was found, so there is no candidate configuration and nothing to realize.

## 1. Encoder validation

All of this passed. Logs are in `logs/`.

### Controls (`logs/controls.log`, `logs/controls_extra.jsonl`)

Every satisfying model was re-checked by the independent checker `symcheck.py` (or by
`modelcheck.py` for D3), which tests symmetry, the A4 and Grassmann–Plücker axioms on all
4- and 5-sets, the centre facts, the labelling normal form, and no convex K-set.

- **4-fold, 16 points, K = 6: SAT.** The model checks out (largest convex subset 5). The
  hexagon-free 4-fold class is non-empty, as in Subercaseaux et al. 2025.
- **5-fold with the centre in the set, 16 points, K = 6: SAT.** The model checks out. The
  5-fold class is non-empty.
- **The requested "k = 6 at 17 points with 3-fold symmetry" cannot be posed.** A 3-fold
  symmetric set has orbits of size 3 plus possibly the centre, so its size is 0 or 1 mod 3,
  and 17 is 2 mod 3. I used ES(6) = 17 controls instead, and all are UNSAT as required:
  - 3-fold, 18 points (`n18k6m3`);
  - 6-fold, 18 points (`n18k6m6`);
  - D3, 21 points (`n21k6d3`).
- **ES(5) = 9 controls: all UNSAT** (`n9k5m3`, `n9k5m9`, `n10k5m3c`, `n12k5m3`, `n9k5d3`).
  `n8k5m8` and `n9k6d3` are also UNSAT; a single orbit of 8, or a D3 6-orbit, is cocircular
  and therefore convex.
- **Small positive controls: all SAT, with checked models.** These are `n6k5m2`,
  `n6k5m3`, `n8k5m2`, `n8k5m4`, `n9k6m3`, `n12k6m3`, `n13k6m3c`, `n21k7d3` and `n27k7d3`.
- **3-fold hexagon-free answers: `n15k6m3` and `n16k6m3c` are UNSAT.** No source confirms
  or refutes these. Exact annealing over real 3-fold 15-point sets never got below one
  convex-hexagon orbit (6 restarts × 4,000 steps; `logs/anneal_n15k6c3.json`), which is
  consistent with UNSAT.

**Labelled model counts (`logs/enum16.log`).** The normal form fixes neither the orbit
labelled 0 nor the mirror image. Exhaustive enumeration over the orientation variables gives
528 models for `n16k6m4` and 2,796 for `n16k6m5c`.
- 528 = 4 × 2 × 66 (orbit choices × mirror images × 66).
- 2,796 = 3 × 932 = 6 × 466. Under the same ×(orbits × 2) rule this would be 466 classes,
  not Subercaseaux et al.'s 948 (`plan/es7_critique.md` item 12 says the paper also gives 932).
- I did not compute isomorphism classes, so this is no comparison either way. The control
  required only that both classes be non-empty, and both are.

### Saved models (`logs/saved_models.jsonl`)

Each saved projected model in `inputs/enum/` was checked three ways: it extends to a model
of the regenerated CNF (CaDiCaL under assumptions), it passes `symcheck.py`, and where a
`.brute` file exists, the brute-force list equals both the saved list and a fresh
`enum_models` enumeration. All files passed:
- `n16k6m4`: 30/30;
- `n16k6m5c`: 30/30;
- `n32k7m2`: 40/40, and the 5 `n32k7m2_seeds`, with largest convex subset 6;
- `n6k5m2`: 3/3, `n6k5m3`: 8/8, `n8k5m2`: 8/8 and `n8k5m4`: 8/8. For each of these, an exhaustive `enum_models` run on the regenerated CNF returns exactly the saved set;
- the empty files `n8k5m8`, `n9k5m3` and `n9k5m9` match UNSAT CNFs, and their `.brute` files are empty too.

### Exact-symmetry validation (`tools/symval2.py`, `logs/val_*.json`)

**Exactness.** Points are Eisenstein integers a + bω with ω = e^{2πi/3}, so the rotation
R(a,b) = (−b, a−b) and the reflection S(a,b) = (a−b, −b) are exact integer maps.
Orientations come from exact integer determinants, which have the same sign as the
Euclidean ones.

**Per sample:**
- The normal-form labelling of `symcnf.py` is applied geometrically (sector and angle
  order).
- The orientations are mapped to CNF variables. A sign conflict in the map counts as a
  failure.
- `cnfeval` decides the CNF under that assignment exactly. The convexity flags form a Horn
  system once the orientations are fixed, so the least model decides it.
- `geomcount` counts group orbits of r-subsets in convex position, using exact convex hulls
  and no chirotope logic.

**Required for every sample:**
- every orientation-only clause holds (axioms, centre facts, sector and order);
- the number of true conv_r flags equals the number of orbits of convex r-sets, for
  r = 4, 5, 6;
- the number of falsified K-set clauses equals the number of orbits of convex 7-sets;
- SAT holds exactly when there is no convex K-gon.

| CNF | samples | map conflicts | mismatches | K-gon-free samples (all accepted) |
|---|---|---|---|---|
| `n33k7m3` (3-fold, 33) | 100 | 0 | 0 | 0 (2,112 to 150,970 convex-7 orbits) |
| `n33k7d3` (D3, 33) | 100 | 0 | 0 | 0 (2,084 to 202,608 convex-7 orbits) |
| `n33k7m3refl` (3-fold + reflection, exact D3 samples) | 60 | 0 | 0 | 0 (1,963 to 362,294 convex-7 orbits) |
| 14 smaller CNFs (`logs/val_small.jsonl`): 3-fold `n6k5m3`, `n9k6m3`, `n12k6m3`, `n15k6m3`, `n18k6m3`; D3 `n9k5d3`, `n9k6d3`, `n15k6d3`, `n21k7d3`, `n27k7d3`; and four `*m3refl` CNFs | 100–400 each | 0 | 0 | 89 (n6k5m3), 36 (n9k6m3), 2 (n12k6m3), 8 (n21k7d3), 2 (n21k7m3refl) |

**Realizable positive controls near the target size:**
- Annealing over exact D3 sets found a heptagon-free D3 **27-point** set
  (`logs/anneal_n27k7d3.json`).
- `check_set.py` maps it into `n27k7d3`, which then evaluates to SAT. All convex-r orbit
  counts match.
- Annealing likewise found a realizable 3-fold hexagon-free 12-point set.

**Mutation test (`logs/mutation_tests.jsonl`).** The validator detects:
- a flipped centre-fact unit and a flipped symmetry-breaking unit (100% of samples);
- a deleted K-set clause, or a deleted top-level convexity definition (31–39% of samples);
- but not a deleted level-4 definition for an orientation pattern that the centre facts
  already exclude, which is expected.

## 2. Cube-and-conquer driver (`tools/cnc2.py`, `tools/ccworker.cpp`)

**Fixes over `tools/cnc/cnc.py`:**
- **One global heap, keyed on (depth, budget, sequence).** The shallowest open cube is
  always handed out next, and cubes at the same depth go first-in first-out. There are no
  per-worker LIFO queues, so no cube can starve.
- **Exact weights.** The driver keeps integer counts of closed cubes per depth. It logs the
  closed weight as an exact fraction and a 30-digit decimal, and checks
  closed + open + running = 1 exactly at every log line.
- **Splits on orientation variables only.** CaDiCaL's own `lookahead()` can pick auxiliary
  flags, so `ccworker` does its own look-ahead. Under the cube, it propagates
  cube ± x for up to 400 free orientation variables, sampled with weight by occurrence. It
  takes the largest (n₊+1)(n₋+1), or any failed literal.
- **Orientation variables are frozen**, so they are never eliminated.
- **Budgets grow:** each child gets its parent's budget × 1.2 (base 10,000 conflicts, cap
  2·10⁶), and an unsplittable cube is retried with a bigger budget.
- **Every closed cube is logged** to `closed.jsonl`.
- `verify_tree.py` checks that the closed and open cubes form an exact partition: a binary
  tree with complementary children on fresh variables, and leaf weights summing to 1.
- `lratcube.py` re-proves closed cubes from scratch, solving the CNF with the cube as unit
  clauses and LRAT output, and checks each proof with lrat-check. `lrat_full.sh` does the
  same for a whole CNF.

**End-to-end test.** On `n18k6m3` (ES(6) control) with tiny budgets, the driver closed all
162 cubes. The tree verified, the weight was exactly 1/1, and 3 of 3 spot-checked cubes
passed lrat-check.

## 3. 3-fold, 33 points (`runs/c3_n33k7/`)

Still running when this was committed. A later commit adds the results.

## 4. D3, 33 points (`runs/d3_n33k7/`)

**The class.** Under D3, 33 = 6a + 3b + c with c ∈ {0, 1}. Each mirror line through the
centre carries b points, so general position forces b ≤ 2, and the only solution is 5
orbits of 6 plus 1 orbit of 3 on the mirror axes.

**The encoding (`d3cnf.py`).**
- It uses the 3-fold normal form, with the 3-orbit as orbit 0 and its point (0,0) on mirror
  M.
- The reflection in M acts on labels as S(0,r) = (0,−r) and S(j,r) = (11−j, −r−1), and fixes
  the centre. The derivation is in the file.
- There is one variable per D3-orbit of triples, and reflections carry a sign flip.
- Axioms and convexity flags are per D3-orbit.
- The result has 232,406 variables (1,017 orientation) and 4,760,236 clauses.

**Result.**
- The cube-and-conquer run closed the root cube in its first job: UNSAT within the
  10,000-conflict budget, about 180 s wall under load.
- A from-scratch solve with LRAT (`--elim=0`) gave UNSAT in 15.8 s CPU, with a proof of
  171 MB. lrat-check printed `c VERIFIED` (exit 0) on the unmodified CNF
  (`logs/lrat_n33k7d3.log`).
- **Cross-check.** The 3-fold CNF from `symcnf.py`, unchanged, plus binary clauses
  chi(Sa,Sb,Sc) = −chi(a,b,c), is also UNSAT (`logs/solve_n33k7m3refl.log`). That
  construction shares only the label rule with `d3cnf.py`. On 21, 15 and 9 points the two
  constructions agree (`logs/c3refl_small.jsonl`). The LRAT proof of the cross-check CNF also passed lrat-check (`logs/lrat_n33k7m3refl.log`).
- **Third construction.** `d3cnf.py --kgon direct` writes each 7-set clause over the 35
  conv₄ flags of its 4-subsets, with no conv₅/conv₆ layer. It also passed the exact
  validation (60 samples, 0 mismatches, `logs/val_n33k7d3direct_d3.json`), and it is UNSAT
  with an LRAT proof that lrat-check verified (`logs/lrat_n33k7d3direct.log`).
- **Annealing.** Exact annealing over real D3 33-point sets
  (`logs/anneal_n33k7d3.json`, 3 restarts × 2,500 steps) got no lower than 24
  convex-heptagon orbits. That is consistent with UNSAT. On 27 points the same annealer
  found heptagon-free D3 sets at once.

**What this does and does not show.** It is LRAT-checked UNSAT of `n33k7d3.cnf`. Read
through the encoding, it says no CC-system (acyclic uniform rank-3 oriented matroid) on the 33
points plus the auxiliary centre, with this D3 symmetry and labelling, is free of convex
7-gons. Hence no real 33-point set in general position with exact D3 symmetry is free of
them either. That reading is only as good as the encoding. The encoding is tested
(controls, exact random D3 sets, a realizable 27-point positive control, mutation tests,
and agreement with two other constructions of the same instance), but it is **not formally verified**. So
this is not a theorem.

## Files

- `tools/`: everything written for this task. `build.sh` builds the C/C++ tools against a
  CaDiCaL build. The generators come from `../../tools/symmetric/symcnf.py` (unchanged) and
  `tools/d3cnf.py`.
- `logs/`: controls, validation, LRAT logs, annealing, the 10-minute status snapshots of the
  3-fold run, and CNF hashes.
- `runs/c3_n33k7/`, `runs/d3_n33k7/`: the cube-and-conquer outputs. These are
  `progress.log` (30-minute records), `events.log`, `closed.jsonl`, `state.json` (open
  cubes; resumable), `verify_tree.json` and `lrat.jsonl`.
- `summary.json`: the machine-readable summary.
- The CNFs (up to 344 MB) are not committed. Regenerate them with
  `python3 tools/symmetric/symcnf.py 33 7 3 -o n33k7m3.cnf --map n33k7m3.json`,
  `python3 results/E/tools/d3cnf.py 33 7 -o n33k7d3.cnf --map n33k7d3.json` and
  `python3 results/E/tools/c3refl.py n33k7m3.cnf n33k7m3.json n33k7m3refl.cnf`. Compare
  against `logs/cnf_sha256.txt`.
