# C3SPOT: from-scratch spot-check of the 3-fold class (m = 11, k = 7): 2,120 of 2,120 pass

One local machine (Apple M5 Pro), 2026-10-28, 18:11 to 21:16 UTC, 10 lanes. A random sample of the certified pieces
behind `results/C3FINAL` was solved again from scratch, and the new results were compared with the stored records.

## Sample (`units6.tsv`)

- **Population.** Every certified record that is not a σ-cube record and has a node name, in the 280 record files of the final
  composition (`results/C3FINAL/compose_files.txt`, tree at f788780c). That is 116,345 distinct nodes in 14 source
  directories. These include σ-cube-refined nodes (names containing `__`): 716 of the 3,084 sampled nodes and 485 of the
  2,120 re-solved ones are of this kind.
- **Draw.** Python `random.Random(20261028)`:
  - 6 nodes from every source directory;
  - 3,000 more drawn uniformly from the rest;
  - all 3,084 shuffled together.
- **Per row.** Each row holds:
  - the node;
  - the `close_tree.py` options `--jobs 1 --caps 3600 --cadopts=--sat --hours 0.02`;
  - the CNF sha256 stored in the original record;
  - the record file the node came from.

## Method (`lane6.sh`, `run_ct.py`)

- **Re-solving.** Each lane takes the next unclaimed row (an atomic `mkdir` claim) and runs C3U2 `close_tree.py`
  (cad4e050) on the node through `run_ct.py`, without changes. This rebuilds the piece's CNF from the base CNF
  (`p cnf 168399 4154921`, sha256 `bf0e502e…6cdd6da`) and the node name. It then solves the piece with CaDiCaL 3.0.1
  (`--sat` configuration, cap 3,600 s), writing an LRAT proof.
- **Proof checking.** Every proof is checked by both lrat-check (E2 patch) and cake_lpr (`CML_HEAP_SIZE=12000`,
  `CML_STACK_SIZE=2000`). All are fresh output files; nothing from the original runs is reused.
- **Stopping.** Lanes take no new row within 5 minutes of the end time. Every claimed row finished.

The rows are processed in their shuffled order, so the 2,120 rows solved in the window are a random subset of the
sample.

## Result (`out.jsonl`, `summary.md`)

A row passes when all four of these hold:
- the solver says UNSATISFIABLE;
- lrat-check prints `c VERIFIED`;
- cake_lpr prints `s VERIFIED UNSAT`;
- the sha256 of the rebuilt CNF equals the one in the original record.

| record source | re-solved | all checks pass | median solve s |
|---|---|---|---|
| C3COMP1 | 3 | 3 | 152 |
| C3H1 | 5 | 5 | 481 |
| C3H1/LOCAL | 10 | 10 | 689 |
| C3S0 | 15 | 15 | 3 |
| C3W3 | 888 | 888 | 3 |
| C3W3S | 6 | 6 | 44 |
| C3W4 | 326 | 326 | 10 |
| C3W5 | 13 | 13 | 58 |
| C3W6 | 57 | 57 | 180 |
| C3W6/LOCAL | 21 | 21 | 224 |
| C3W7 | 18 | 18 | 608 |
| C3W7/LOCAL | 32 | 32 | 711 |
| C3WAVE1 | 392 | 392 | 3 |
| C3WAVE2 | 334 | 334 | 3 |

**2,120 re-solved, 2,120 pass, 0 other, 0 timeouts.**
- Time: solving took 22.9 core-hours and checking 7.1. The longest solve took 1,210 s.
- What it shows: the stored verdicts of the sampled pieces are reproducible from the base CNF alone.
- What it suggests: with 0 failures in 2,120 draws, the share of bad records is small. A rule-of-three bound (below
  0.15% at 95% confidence) is only indicative here. The draw was stratified (6 per source directory, then uniform), and
  only the first 2,120 rows of the shuffled list were solved in the time window. The check is not exhaustive. It adds to
  the per-record checks at solve time and the double composition; it does not replace them.

## Files

- `units6.tsv`: the sample.
- `lane6.sh`: the lane script.
- `run_ct.py`: the runner, as in `results/C3W7/LOCAL2`.
- `out.jsonl`: one record per re-solved row. It has the same fields as the original records, including `cnf_sha256`,
  `proof_sha256`, `lrat_check` and `cake_lpr`.
- `summary.md`: the table above, from `python3 spot_summary.py WORK units6.tsv`, run on the lane output directory.
- `driver*.log.tail`: the last lines of each lane log.
