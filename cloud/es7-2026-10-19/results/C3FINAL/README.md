# C3FINAL: final double composition of the 3-fold class (m = 11, k = 7): covered

One local machine, 2026-10-28, 17:57:55 to 17:58:26 UTC (`tools.txt`). Same method as `results/C3COMP1` part 1:
`results/C3U2/tests/frontier_cmp.py` runs C3U2 `compose.py` (cad4e050) and C3AUDIT3 `mycompose.py` (the fixed version,
5336f631) on the same records, without changing either, with sha checks on and `--mirror-h6` (`run_final.sh`).

## Inputs

Every record file of the results tree at f788780c (a `git archive` snapshot), as listed in `compose_files.txt`: 280 files,
128,803 records. They are all of `results/C3COMP1/compose_files.txt`'s sources up to now plus every `out.jsonl`,
`recheck*.jsonl` and `presplit.jsonl` of `results/C3W6`, `results/C3H1` and `results/C3W7`, including the local runs
(`C3W6/LOCAL`, `LOCAL2`, `LOCAL3`, `C3H1/LOCAL`, `LOCAL2`, `C3W7/LOCAL`, `LOCAL2`). Base CNF `gen_case.py 11 7 none`:
`p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`.

## Result (`C3FINAL_mirrorh6.json`, `C3FINAL_mirrorh6_roots.tsv`, `run_final.log`)

| | C3U2 `compose.py --mirror-h6` | `mycompose` (fixed), same 910 roots |
|---|---|---|
| certified records / nodes | 116,883 / 116,741 | 116,883 / 116,741 |
| CNF sha256 re-derived from BASE and matched | all 116,883 | all 116,883 |
| certified σ-cube nodes | 26,748 | 26,748 |
| σ splits used | 1,747 | 1,752 (no H6 mirror) |
| depth-2 roots / open | 910 / **0** | 910 / **0** |
| uncovered frontier under the 910 roots | 0 | 0 |
| class covered | **yes** (`"class_covered": true`, empty frontier) | see below |

Root status differences between the two composers: **0**.

`mycompose` has no H6 mirror, so its own tree also holds the 720 mirror-image H6 depth-2 roots that the reduced cut drops
(1,630 roots instead of 910; `results/C3COMP1`). Its whole-tree line (`"class_covered": false`, 2,260 uncovered frontier
nodes, for example `0s0-1s1_10_9_5s0-6s1`) is about those roots only: none of its uncovered nodes lies under the 910 roots
(`"frontier_mycompose_in_roots": 0`). As in `results/C3U2` and `results/C3COMP1`, it is read on the 910 kept roots.

## What this closes

The reduced cut rests on Lemma H6M (`results/C3AUDIT2`), and the tree on the C3-S normal form
(`results/C3-S/soundness.md`). With those, every 3-fold-symmetric set of 33 points in general position (11 orbits of a
rotation by 120°) has 7 points in convex position. Every certified record used here was accepted by both proof
checkers when it was solved (lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`). The records carry those
verdicts; the proofs themselves are not stored. The mirror class was closed earlier (`results/FINAL` and its acceptance
passes `results/V3T`, `results/V3A` to `results/V3E`, `results/V3Z`).
