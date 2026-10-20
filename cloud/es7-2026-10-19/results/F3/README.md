# F3: scaled novel-realizable-pool pipeline, seeds in [3000000, 4000000)

Cloud VM, 20 October 2026, 02:36–06:20 UTC. Machine: 4 cores, 15 GB RAM, Linux 6.18 (`env.txt`).
Only seeds in [3000000, 4000000) were used.

## Bottom line

- **No candidate.** No 33rd point was found for any 32-point set. No free face and no SAT answer
  came up anywhere, so nothing needed realizing.
- **3 new realized (7,5,7)@26 sets:** `gg3000002_1`, `gg3000002_2` and `gg3000003_7`. Each has
  exact integer coordinates and was re-checked exactly and by brute force: general position,
  max cap 4, max cup 6, largest convex subset 6, 0 signotope-axiom violations.
- **All 3 are new order types.** Their canonical fingerprints (relabelling + reflection) differ from
  each other and from all 26 sibling 26-sets committed so far (F2 ×8, F2/s2 ×9, F4, F5, F6;
  `data/other_runs_fingerprints.jsonl`).
- **64 deep-below 32-point sets were built from them, 62 distinct order types.** None is in the
  8,537-set input pool. Results:
  - All 64 are heptagon-free by exact brute force.
  - All 64 are **abstractly saturated**: ext_solve gives UNSAT at all 33 x-positions, with no
    UNKNOWN.
  - 21 of them have a realization with |coordinates| < 2^27, and each of these 21 is also
    **geometrically saturated**: sat.c finds 0 free faces, and the face count matches Euler's
    formula.
  - For the other 43, compression failed, so only the abstract test applies. The abstract test
    covers every x-position: any geometric 33rd point gives a model of the one-point extension
    CNF.
- These are claims about specific CNFs and exact point sets, not theorems. The encodings are not
  formally verified, and the UNSAT answers have no LRAT certificates.

## What ran

| arm | seeds | CPU | abstract models | complete 26-sets |
|---|---|---|---|---|
| F2 `grow_guided.py` (model-guided growth, prefix_server oracle) | 3000001, 3000002, 3000003 | 8.1 core-h | 7,983 prefix-constrained models (SAT queries); 3,792 realizer calls; 23 chains | **3**: 3000002 ×2, 3000003 ×1 |
| F2/s2 `arm_f.py` (SAT-guided insertion, default options) | 3100001 | 0.75 core-h | 661 restarts | 0 (max 22/26 points); stopped, core reassigned to grow_guided |
| KPH-style: F2/s2 `gen_models.py` + `realize_models.py` (results/F realizer, 5 CPU-s/model) | 3200001–3200016 | 2.2 core-h | 1,600 generated, 1,421 sent to the realizer | **0 / 1,421** |

**Realization rate (KPH-style arm): 0 / 1,421.** The 95% upper bound is about 2.1e-3 (rule of
three). This is consistent with KPH's ~1.6e-4, which predicts about 0.23 realizations here. It
cannot confirm or refute their rate, and our per-model budget (5 CPU-s, ins-ff + LP) differs from
Localizer's 15 s. Model-guided growth is far more productive: about one new realized 26-set per
2.7 core-hours.

## Reproduction of F2 (step 2)

I rebuilt CaDiCaL from GitHub master, `sat.c`, `ext_solve.cpp`, `prefix_server.cpp`, `brute26.c`,
`brute.c` and `brute_kgon.c`. The CNFs were regenerated with `gen_etv.py 26 5 7 7` and
`gen_cnf.py 33 7`. I then reran F2/s2's `pipeline.sh` on its run1 sets F22_106 and F22_162
(`data/repro_F2s2/`). The post26 records, brute26 output, build32 records and the saturation
result are identical to F2's: 109,337 faces, 0 bad, 33/33 UNSAT. The only difference is the
compressed coordinates, which come from the time-budgeted realizer; they are exact re-checked
realizations of the same chirotope.

## Per-set results (`data/summary.json`, `data/sets/<id>/`)

| 26-set | fingerprint | conv. A (given x-direction, 6-cap deep below) | conv. B (all sweep directions with cap ≤ 4) |
|---|---|---|---|
| gg3000002_1 | 1e6478898e0b114e1e84 | 1 set: geometric saturated, abstract 33/33 UNSAT | 32 of 650 directions → 32 sets: all 33/33 UNSAT; 10 compressed → all geometric saturated |
| gg3000002_2 | c0458eb8fb9c4b153ec2 | 1 set: abstract 33/33 UNSAT; geometric not run (compression failed) | 9 directions → 9 sets: all 33/33 UNSAT; 4 compressed → all geometric saturated |
| gg3000003_7 | 990901f3597bad54e531 | 1 set: geometric saturated, abstract 33/33 UNSAT | **partial:** process26 was stopped at 06:00 for time after 20 sets, all 33/33 UNSAT; 5 compressed → all geometric saturated |

Every compressed set was also tested abstractly and gave 33/33 UNSAT. Brute force (brute_kgon and
brute26) found 0 convex 7-subsets in every exact and compressed 32-set. The 32-set fingerprints
are in `data/fingerprints32.jsonl`.

## Notes and deviations

- **Upstream scripts changed mid-run.** F2's scripts are called live from `results/F2`. F2/s2
  updated `build32.py` and `saturate32.py` during my run (commits a76eb3b, 9c80824, …), and my
  pull brought them in. gg3000002_1 conv. A used the earlier version; later sets used the newer
  one. The changes only skip already-done ids, try a 26-set recompression first, and run sat.c
  only when coordinates are below 2^27.
- **Compression bug fixed.** `build32.py` could record a "compressed" realization above 2^27
  (2^52 for gg3000002_2). `scripts/conva_fix.py` now retries the realizer (6 seeds × 120 s) and
  otherwise marks the set uncompressed. `conva.sh` is pipeline.sh with this step added.
- **Recompression pass had no effect.** A later pass (`recompress_convB.py`, 3 seeds × 60 s) tried
  13 conv. B sets, compressed none, and was stopped.
- **Other scripts.** `process_set.sh` is the per-set driver, `watch.sh` the queue, `kph_loop.sh`
  the KPH-style arm, `fingerprint.py` the canonical fingerprints (results/F `chiro.canonical_form`),
  and `collect.py` builds the summary.
- **Not committed.** No CNF or proof files, and nothing over 50 MB.
