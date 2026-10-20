# F4: scale-out of the F2 novel-realizable-pool pipeline (seeds 4000000–4999999)

**Result: no new realized (7,5,7)@26 set, so no new 32-point deep-below sets and no 33-point
candidate.** One new heptagon-free 26-point set was realized exactly (gg4000008_5). It has max
cap >= 5 in every sweep direction, so neither deep-below convention applies to it.

## Where and what ran

- One cloud VM (`env.txt`: 4 cores, 15 GB), 2026-10-20 02:36–06:05 UTC. The container restarted
  once (~03:00); all runs were relaunched with fresh seeds, and the logs from before the restart
  were kept.
- Built from source: CaDiCaL (master; used as libcadical.a by ext_solve.cpp and prefix_server.cpp),
  `tools/trackA/sat.c`, F2 `brute.c`, F2/s2 `brute26.c`, `tools/trackB/brute_kgon.c`. pysat
  (cadical195) and highspy were used for the Python arms.
- CNFs: `gen_etv.py 26 5 7 7` (17,831 vars, 222,991 clauses) and `gen_cnf.py 33 7` (47,002 vars,
  679,038 clauses). These are the same as F2.
- Seeds used: 4000001–4000008, all inside the assigned range.

| arm (script) | seeds | effort | complete 26-sets |
|---|---|---|---|
| grow_guided.py (F2, model-guided growth) | 4000001, 4000002 (killed at the restart), 4000007, 4000008 | 22 finished chains, ~5.7 core-h | 1 (gg4000008_5, via the hybrid realizer step) |
| arm_f.py (F2/s2, SAT-guided exact insertion), defaults | 4000003 | 558 restarts | 0 (max 22 placed) |
| arm_f.py `--jitter 0.3 --extra-props 2 --smart-bt` | 4000006 | 3,019 restarts, ~2.7 core-h | 0 (max 25 placed, once) |
| gen_models.py + realize_models.py (validated realizer, 4 CPU-s, ins-ff,lp) | 4000004, 4000005 | 3,000 distinct abstract models, 12,263 CPU-s | 0 |

The F2 logs do not say which options produced F2's realized sets. F2's names (gg401_5, gg402_3,
F22_106, F22_162) only show that they came from grow_guided and from arm_f. Both arms were reused.

## Realization rate

- Out of 3,000 abstract (7,5,7)@26 models, 0 were realized (all 3,000 are OK under brute26 26 5 7 7).
- At KPH's rate of about 1.6e-4 per model, the expected number is 0.48. P(0 | KPH rate) is about
  0.62, so this sample does not contradict KPH.
- Our 4 CPU-s budget is a quarter of KPH's 15 s per model. The 95% upper bound from 0/3000 is
  about 1.0e-3 per model at this budget.
- Best insertion progress: 18 of 26 points placed. The histogram is in `stats.json`.
- The generators that build points directly do better than realizing abstract models. Arm F got
  within one point of 26, and grow_guided produced one complete heptagon-free set in ~5.7 core-h.

## The new 26-point set gg4000008_5

`data/sets26/gg4000008_5.pts` (integers below 2^19).
- Exactly checked: distinct x, general position, and largest convex subset 6. That is
  chiro.largest_convex_subset and brute.c, both giving 6. Signotope axioms: 0 violations.
- Canonical order-type fingerprint `d336c15c4178610029e31389a3c5f79e12757c21`, which differs from:
  - all four F2 / F2-s2 sets (F22_106, F22_162, gg401_5, gg402_3);
  - the five sibling sets on the branch at 06:00 UTC (F3: gg3000002_1, gg3000002_2, gg3000003_7;
    F6: gg6000202_1, gg6000202_2).
- It came from the hybrid step: the validated realizer realized the labelled chirotope of the
  current model, but the x-order of the result is not the model's. In its own x-direction it has
  max cap 6 and max cup 6.
- It is not a (7,5,7) set in any direction:
  - process26.py checked all 650 combinatorially distinct sweep directions, and every one has max
    cap >= 5;
  - s2's build32.py finds neither a 4-cap frame nor a 4-cup frame.
  So the deep-below lemma gives no 32-point set in either convention (`files32: 0`), and there is
  nothing to saturation-test. It is not a realization of an abstract (7,5,7) signotope, and it is
  not counted as one above.

## 32-point saturation results

- No new 32-point sets were built, because no new (7,5,7)@26 set was realized. Nothing was found
  by either the geometric face sweep or the one-point extension SAT, and there are no candidates.

## Controls (`controls/`)

- `F22_106_repro`: F2/s2 pipeline.sh on F22_106 reproduces all of the following:
  - sign hash 42629b224dde2249 and brute26 OK;
  - the same deep-below 32-set (D = 2^60, lcs 6);
  - sat.c: 109,337 faces, equal to the Euler count, with 0 bad candidates;
  - ext_solve: 33/33 UNSAT;
  - brute 32 OK.
- `gg401_5`: the F4 end-to-end processor (`scripts/process_new26.sh`, with the novelty check
  bypassed) reproduces F2's 5 direction-scan deep-below 32-sets, plus the s2-convention set (the
  same order type as d4). All 9 files pass:
  - general position, lcs 6, brute_kgon 0 convex 7-sets;
  - ext_solve 33/33 UNSAT;
  - sat.c 0 bad candidates on the files below 2^27.
  A compression retry was added afterwards so that more order types get the face sweep.

## Caveats

- UNSAT answers here are claims about single CNFs, not certified: no LRAT proofs were produced.
  The encodings are not formally verified.
- One bug was fixed during the run: an empty glob when a set has no cap <= 4 direction. It did
  not affect any result; the set was re-processed after the fix.

## Files

- `scripts/`:
  - `process_new26.sh`: verify, fingerprint, both conventions, check32;
  - `watch26.sh`, `fingerprint.py`, `jsonl2pts.py`, `stats.py`.
- `data/logs/`: per-arm logs. `am/models_all.sha1` is the sha1 of the 3,000 model lines; the
  models themselves are not committed.
- `data/sets26/`, `stats.json`, `progress.md`.
