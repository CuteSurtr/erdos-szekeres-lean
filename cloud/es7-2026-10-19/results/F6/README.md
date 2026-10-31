# F6: scale-out of the F2 novel-realizable-pool pipeline (seeds 6000000–6999999)

Nothing here is a claim about ES(7). No candidate 33-point set was found.

## Where and what ran

- Cloud VM, 4 cores, 15 GB (`env.txt`), 02:36–06:15 UTC on 20 Oct 2026. Generation ran
  02:39–05:50. Post-processing ran alongside it and finished at about 06:03.
- Tools were rebuilt from source: CaDiCaL master `c6073042`, plus `tools/trackA/sat.c`, F2/s2
  `brute26.c`, F2 `brute.c`, `tools/trackB/brute_kgon.c`, `results/A/scripts/ext_solve.cpp` and
  F2 `prefix_server.cpp`. CNFs came from `gen_etv.py 26 5 7 7` (17,831 vars, 222,991 clauses) and
  `gen_cnf.py 33 7` (47,002 vars, 679,038 clauses). CNF files are not committed.
- **Reproduction:** the rebuilt F2/s2 `pipeline.sh` on F22_106 and F22_162 matches
  F2/s2/data/run1 (`data/controls/repro_F2s2`). F2's `process26.py` on gg401_5 gives the same
  5 cap-4 directions and 5 deep-below sets.
- **Fingerprint control:** canonical order-type fingerprints (`chiro.canonical_form`, relabelling
  plus reflection) are unchanged under a 90° rotation and a reflection
  (`data/controls/fingerprint_controls.txt`).
- Every seed used is in [6000000, 7000000). Realizer seeds are 6500000+i and 6600000+k.

## Generators (scripts/run_arms.sh, run_arms2.sh; logs in data/run)

| arm | seeds | effort | complete 26-sets |
|---|---|---|---|
| F2 grow_guided.py (model-guided growth) | 6000201–205, 6000211–214 | 19 finished chains, about 1 core for 3.2 h plus 1 core from 03:17 | **2** (both from seed 6000202, chains 1 and 2) |
| F2/s2 arm_f.py, default options | 6000001–002 | 846 restarts (02:39–03:17) | 0 (best 22/26 placed) |
| arm_f `--jitter 0.3 --extra-props 2 --bt-depth 4` | 6000101–102 | 542 restarts | 0 (best 23) |
| arm_f `--jitter 0.3 --extra-props 2 --smart-bt` | 6000111–114 | 1,641 restarts (03:17–05:15) | 0 (best 25) |
| KPH-style: gen_models.py → validated realizer (results/F, ins-ff+lp, 4 CPU-s/model) | 6000301; realizer 6500000+i | 3,000 distinct models (439 s); 1,883 realization attempts, 7,733 CPU-s | **0 / 1,883** |

Grow chain end sizes: 17:1, 18:1, 19:6, 20:2, 21:3, 22:2, 23:2, 26:2.

**Realization rate:**
- **Abstract-first (KPH-style):** 0 of 1,883 abstract (7,5,7)@26 models were realized. At KPH's
  rate of about 1.6e-4 per model, we would expect about 0.3, so this result agrees with KPH's rate
  and is too small a sample to estimate the rate.
- **Caveats:**
  - Our budget is 4 CPU-s per model, against Localizer's 15 s.
  - The models come from one blocking-clause sequence (rebuilt every 50 models), so they are
    correlated.
  - Insertion stalled at 8–17 of 26 points (mode 12).
- **Geometry-first:** grow_guided realized 2 sets in 19 chains (about 0.1 per chain). It builds
  exact points as it goes, so this rate is not comparable to a per-abstract-model rate.

## New realized 26-point sets (data/sets26)

| set | source | checks | fingerprint | new vs F2 (22 sets) | vs F3–F5 at 05:52 |
|---|---|---|---|---|---|
| gg6000202_1 | grow_guided 6000202 chain 1 (dfs, 916 s) | distinct x, general position, cap 4, cup 6, lcs 6, brute 0 axiom violations | 73018d566e82b37c | **new** | no match |
| gg6000202_2 | grow_guided 6000202 chain 2 (dfs, 358 s) | same | 7a99a99767186a46 | **new** | no match |

So there are 2 new distinct 26-point order types (`data/fingerprints26_final.json`, `data/siblings_fp_check.txt`).

## 32-point deep-below sets and the 33rd-point tests (data/sets32)

Both conventions were run:
- **(s2)** F2/s2 `pipeline.sh`: a 6-cap deep below in the x-frame;
- **(scan)** F2 `process26.py`: every combinatorially distinct up-direction with max cap ≤ 4,
  then `check32.py`.

Every 32-point set was checked exactly:
- general position, with largest convex subset 6 (Python ints);
- `brute_kgon` (or brute26 on the 32-point signotope): 0 signotope violations and 0 convex 7-subsets.

| 26-set | 32-sets (distinct order types) | abstract: ext_solve at all 33 x-positions | geometric: sat.c exact face sweep |
|---|---|---|---|
| gg6000202_2 | 17 scan + 1 s2 (17 types; s2 = scan d16) | 18/18: 33/33 UNSAT | **17/17 types swept, 0 free faces** (109,337 faces = Euler count each). 12 via process26 compressions, 5 via `scripts/geom_fill.py` recompression |
| gg6000202_1 | 29 scan + 1 s2 (29 types; s2 = scan d28) | 30/30: 33/33 UNSAT | only **2/29 types swept** (d25, d26), 0 free faces. No exact realization below 2^27 was found for the other 27 (build32 compression, process26 compression, then geom_fill 3 seeds × 40 CPU-s each) |

- **SAT answers:** none. **UNKNOWN answers:** none. **Free faces:** none. So there are no
  candidates.
- Every one of the 46 distinct 32-point order types is **abstractly saturated**: the one-point
  extension CNF is UNSAT at every position. This means no realizable 33rd point exists either,
  as far as this unverified encoding goes.
- The geometric face sweep, an independent exact cross-check, covers 19 of the 46 types.
- These UNSAT answers are solver claims about single CNFs. They are not LRAT-certified (no proofs
  were produced) and they are not theorems.

## Files

- `scripts/`:
  - `run_arms*.sh` launch the workers;
  - `watch_new.sh` → `handle26.sh` → `process_new.sh` take each new set through both conventions;
  - `fingerprint26.py` and `fp32.py` compute the dedupe fingerprints;
  - `geom_fill.py` recompresses and runs sat.c;
  - `realize_models.py` is F2/s2's version with the realizer seed taken from 6500000+i.
- `data/run/` holds the generator logs. The arm F records are gzipped. The 3,000-model file is not
  committed (sha256 prefix dcd6ffe5b86e1458).
- `progress.md` is the timeline.
- Note: the first gg6000202_1 s2-convention run shared a scratch directory with the reproduction,
  so its raw logs also list F22_106 and F22_162. `data/sets32/gg6000202_1/s2conv_*` keep only its
  own records.
