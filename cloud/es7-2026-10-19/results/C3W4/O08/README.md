# C3W4 / O08: wave 4, list W4_one.tsv, shard 8 of 16

**Result: both of my roots are closed: 0s0-3s0_1 and 0s0-4s1_1. Open frontier 0, no childless timed-out node. 128 cubes certified. No SAT, no proof rejection, no memory problem.**

## Setup

One cloud VM, 4 cores, 15 GB RAM, no swap (`env.txt`). Start 11:31:08 UTC on 2026-10-24; END would have been 16:16:08 UTC. The runner started at 11:34:15 and finished both roots at 13:27:40 UTC.

- Tools: a worktree of commit `95cafa93` (C3U tools) at `/opt/c3u`, used unmodified. CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example prints `s VERIFIED UNSAT`), and lrat-check 2e3b2dc with the E2 patch. The sanity check passed: on {1},{-1}, LRAT `3 0 0` is rejected by both checkers and `3 0 1 2 0` is accepted by both. Details are in `tools.txt`.
- Base CNF: `gen_case.py 11 7 none` gives `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da` (matches).
- Roots: rows of `lists/W4_one.tsv` with row ≡ 8 (mod 16). These are rows 8 and 24 (`roots.tsv`). No records were seeded.
- Options: `--jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat`, with a 2.5 h slice per root (`runner.sh`).
- `compose.py` was not run, as the task requires.

## Per root

| row | root | stratum | status | certified | timeouts | splits | solve s | check s | max solve s | wall |
|-----|------|---------|--------|-----------|----------|--------|---------|---------|-------------|------|
| 8 | 0s0-3s0_1 | H6(3,0)/one | **closed** | σ level 2 (6 bits, cap 300): 64 | root and 8 σ-level-1 cubes at cap 1 (as intended) | σ: root on bits [2,4,5]; 8 level-1 cubes on [6,7,8]; 8 children each | 3852 | 2426 | 144.8 | 11:34–12:11 |
| 24 | 0s0-4s1_1 | H6(4,1)/one | **closed** | σ level 2 (6 bits, cap 300): 64 | root and 8 σ-level-1 cubes at cap 1 (as intended) | σ: root on bits [2,3,5]; 8 level-1 cubes on [6,7,8]; 8 children each | 10736 | 2865 | 251.2 | 12:11–13:28 |

Every node stays at layer depth 2, because no layer split was needed. No 6-bit cube timed out at 300 s, so none went to the 600 s layer split. Solve and check times are summed per node over 3 parallel jobs, so they are not wall-clock time.

## Totals per stratum

| stratum | roots | closed | certified cubes | solve s | check s |
|---------|-------|--------|-----------------|---------|---------|
| H6(3,0)/one | 1 | 1 | 64 | 3852 | 2426 |
| H6(4,1)/one | 1 | 1 | 64 | 10736 | 2865 |
| total | 2 | 2 | 128 | 14588 | 5291 |

`out.jsonl` has 164 records: 128 certified, 18 cap-1 UNKNOWN records and 18 σ split records, each with 8 children.

## SAT / rejections / memory

- SAT: none.
- Proof rejections: none. Every certified record has lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`. No record has cake_lpr `none`, so `recheck.jsonl` was not needed.
- Split records with `"children": 0`: none.
- Memory: free memory never went below 2 GB. No OOM and no errors.
