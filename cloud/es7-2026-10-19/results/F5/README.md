# F5: novel realizable (7,5,7)@26 pool, scale-out of F2 / F2-s2 (seeds in [5000000, 6000000))

Ran 20 Oct 2026, 02:36 to about 06:00 UTC, on one cloud VM: 4 cores, 15 GB RAM (`env.txt`).
Seeds used: 5000001, 5000002, 5000003 (arm F), 5000401, 5000402, 5000403 (growth), 5000900
(plain models). Nothing here is a theorem or a counterexample.

## Pipeline (reused from F2 and F2/s2)
- **Tools.** CaDiCaL was built from git master (also used for `prefix_server` and `ext_solve`).
  Also built: `sat.c`, `brute_kgon.c`, F2 `brute.c`, F2/s2 `brute26.c`. pysat (cadical195) and
  highspy came from pip. CNFs: `gen_etv.py 26 5 7 7` (the ETV encoding) and `gen_cnf.py 33 7`
  (the base CNF for the 33rd point).
- **Reproduction (step 2).** I reran F2/s2 `pipeline.sh` on its two realized sets
  (`data/repro_F2s2/`). The 26-point checks and both brute-force outputs are byte-identical to
  F2/s2's. The saturation verdicts are also identical: 109,337 faces (equal to the Euler count),
  0 bad candidates, 33/33 UNSAT. Only the compressed realizations differ, because the realizer is
  time-budgeted.
- **End-to-end control (`data/control_gg401_5/`).** I ran `scripts/process_set.sh` on F2's
  gg401_5. It produced 8 32-point files. All have lcs 6 and no convex 7-subset (brute_kgon), and
  all have 33/33 UNSAT. sat.c ran on the 2 compressed files and found them saturated. This matches
  F2's results.
- **Generators.** See the table below for what each produced.
  - Arm F is F2/s2's SAT-guided exact insertion (`arm_f.py`).
  - Growth is F2's model-guided growth (`grow_guided.py` with `prefix_server`, default options).
  - The plain arm runs F2/s2 `gen_models.py` and then `realize_models.py`: random distinct
    models, then the validated realizer with a 5 CPU-s budget per model.
- **Per new set (`scripts/watch.py` → `scripts/process_set.sh`):**
  - Exact recheck of each realized 26-point set, with two checks: `verify26.py` (Python DP for
    cap/cup, exact largest convex subset, F2 `brute.c`) and `brute26 26 5 7 7`.
  - Canonical order-type fingerprint (`chiro.canonical_form`, which covers relabelling and
    reflection), used for deduplication.
  - **Both deep-below conventions:**
    - (a) F2 `process26.py`: every sweep direction in which the max cap is ≤ 4 gets a 6-cap deep
      below. Results are deduplicated by signotope.
    - (b) F2/s2 `build32.py`: the x-direction, with a 6-cap below (or a 6-cup above after
      reflection).
    - Coordinates ≥ 2^27 were recompressed by the realizer, and each compressed set was rechecked
      exactly.
  - Every 32-point file goes through F2 `check32.py`:
    - general position;
    - exact largest convex subset;
    - brute_kgon over all C(32,7) subsets;
    - sat.c on every face of the arrangement, when |coord| < 2^27;
    - ext_solve, the one-point extension SAT at all 33 x-positions, with no conflict limit.

## Results

| arm (seeds) | CPU time | attempts | realized 26-sets | best partial |
|---|---|---|---|---|
| arm F, default (5000001) | 0.23 h | 356 restarts | 0 | 22 |
| arm F, `--jitter 0.5 --extra-props 2 --smart-bt` (5000002, 5000003) | 3.3 h | 2,584 restarts | 0 | 25 |
| growth (5000401, 5000402, 5000403) | 8.0 h | 17 chains (5,987 model queries) | **2** (seed 5000401, chains 1 and 6) | 26 |
| plain random model → realizer (5000900, niced) | ~2.1 CPU-h | 2,000 models drawn, 1,524 tried | 0 | 19 placed |

- **Arm F.** It was 0 for 2,940 restarts here, while F2/s2's seed 22 found 2 in 162 restarts. On
  this machine growth was clearly the more productive arm, so after 13 minutes I moved one arm-F
  core over to growth.
- **Realization rate per abstract model (KPH reports about 1.6e-4).**
  - Plain arm: 0 of 1,524 models. Expected at KPH's rate: 0.24. This is consistent with KPH and
    is not a measurement; the 95% upper bound is about 2.0e-3.
  - Growth: 2 realizations in 5,987 prefix-constrained model queries (about 3.3e-4 per query).
    The queries are not independent random models, so this number is **not** comparable with
    KPH's. The fair summary is 2 realizations per 8 CPU-h of growth, or 1 per 8.5 chains.
- **New distinct 26-point sets: 2**, `gg5000401_1` and `gg5000401_6`.
  - Both have integer coordinates, distinct x and are in general position. In the x-direction
    each has max cap 4 and max cup 6.
  - The largest convex subset is 6, confirmed three ways: Python exact, `brute.c`, and
    `brute_kgon 26 7` (0 convex 7-subsets out of 657,800, `data/brute_kgon26.txt`).
  - brute26 26 5 7 7 returns OK for both.
  - Their fingerprints (`data/f5_fingerprints.txt`) differ from F2's 4 original sets, and also
    from all 27 sets in F2, F2/s2, F3, F4 and F6 on the branch as of 05:55
    (`data/sibling_fingerprints.txt`).
- **32-point deep-below sets** (`data/sets/<name>/`):

| 26-set | exact 32-sets | distinct order types | brute_kgon 7 | lcs | abstractly saturated (33/33 UNSAT) | sat.c saturated (compressed realization) |
|---|---|---|---|---|---|---|
| gg5000401_1 | 42 (41 directions + x) | 41 | 0 everywhere | 6 | 41/41 types (79/79 files) | 36/41 types (37 files) |
| gg5000401_6 | 17 (16 + x) | 16 | 0 everywhere | 6 | 16/16 types (33/33 files) | 15/16 types (16 files) |

  - In both cases the x-direction set has the same order type as one of the direction sets.
  - Every sat.c run reported 109,337 faces, equal to the Euler count, and 0 bad candidates.
  - For 6 order types the recompression found no realization below 2^27, so they were tested only
    abstractly. The abstract test does not depend on the realization, so it is the stronger
    statement.
  - **No free face and no SAT position (no candidates).**
  - None of the 57 new 32-point order types occurs among the 8,537 pool sets
    (`novelty32.json`, F2 `novelty.py`).

## Caveats
- Each "UNSAT" is a claim about one CaDiCaL run on one CNF (`gen_cnf.py 33 7`, with the old
  triples as assumptions). None was LRAT-certified.
- The geometric sweep checks one compressed realization of each order type, not the original
  huge-coordinate set. Different realizations can have different arrangements; the abstract test
  covers all of them.

## Files
- `scripts/`: `process_set.sh`, `watch.py`, `fingerprint.py`, `stats.py`, `archive_set.sh`.
- `data/gen/`: generator logs. `data/gen_stats.json` holds the summaries.
- `data/realized26.jsonl`: the watcher registry. `data/watch.log`.
- `data/sets/<name>/`: the 26-point set, verify26, brute26, fingerprints, process26 and build32
  logs, `check32.jsonl`, `summary.json`, and the `sets32/*.pts` files (exact and `_small`
  compressed).
