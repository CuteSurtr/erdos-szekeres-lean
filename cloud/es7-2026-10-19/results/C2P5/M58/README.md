# C2P5 M58: LIST = C2P5B.tsv, shard j = 8 of N = 50, H = 5.25 h (TASK commit 81cb025f)

Start 2026-10-31 15:10:14Z (epoch 1793459414); END = 1793477414 (20:10:14Z). The lane started at 15:13:20Z and finished every unit at 18:25:48Z (`lane done`), with time to spare.

## Tools and checks (`tools.txt`)
- Built only from the vendored sources with `C2P/vendor/build_tools.sh`. The manifest matched (196 files). Nothing was cloned or downloaded.
  - CaDiCaL 3.0.1, commit c6073042
  - cake_lpr, commit a36874a8
  - lrat-check, commit 2e3b2dc, with the E2 patch
- Sanity checks: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. base.cnf sha256 `b0061e90…d8ff1` and base.json sha256 `2476faff…2b48` both match the expected values.
- Cubes: P1..P8 from `C2C34/l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`): rows of C2P5B.tsv with idx ≡ 8 (mod 50), 14 units

| case | kind | units | certified | timed out (UNKNOWN) | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | Q | 2 | 2 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **total** | | **14** | **14** | **0** | **0** | **0** |

Every unit was UNSATISFIABLE, and both checkers accepted every proof: lrat-check printed `c VERIFIED` and cake_lpr printed `s VERIFIED UNSAT` (heap 8000 MB; no retry was needed).

| unit | kind | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|---|
| P2_3-5 | Q | 489.55 | 57.9 | 344.6 | 3.45 |
| P1_2-5 | Q | 606.81 | 60.1 | 359.2 | 3.45 |
| P1_7-10 | Q | 520.24 | 60.4 | 357.9 | 3.35 |
| P1_2-3-9 | H | 95.41 | 27.3 | 184.9 | 1.23 |
| P1_2-8-9 | H | 226.86 | 56.1 | 328.9 | 3.10 |
| P1_3-5-15 | H | 351.19 | 61.8 | 393.4 | 3.39 |
| P1_4-6-7 | H | 36.37 | 16.4 | 132.5 | 0.22 |
| P1_5-9-10 | H | 25.79 | 15.4 | 129.3 | 0.22 |
| P3_4-15 | Q | 3206.75 | 123.6 | 659.9 | 6.58 |
| P3_1-4-16 | H | 443.64 | 67.8 | 417.9 | 3.56 |
| P3_1-9-15 | H | 552.80 | 65.6 | 381.4 | 3.52 |
| P3_4-7-8 | H | 31.02 | 17.2 | 122.1 | 0.22 |
| P3_5-6-11 | H | 32.47 | 14.4 | 125.7 | 0.22 |
| P3_6-8-9 | H | 27.70 | 15.0 | 132.2 | 0.22 |

Min / median / max over the 14 certified units:
- solve: 25.8 / 289.0 / 3206.8 s
- lrat-check: 14.4 / 57.0 / 123.6 s
- cake_lpr: 122.1 / 336.8 / 659.9 s
- proof size: 0.22 / 3.22 / 6.58 GB

## Resources and anomalies
- The largest solver RSS was 4434 MB (P3_1-4-16). cake_lpr's resident memory was about 8.2 GB at a spot check. There were no memory problems.
- The disk never ran short: the lowest free space seen was 21 GB, while the largest proof (6.6 GB) was being written.
- No SAT result (`/opt/work/SAT_FOUND` never appeared), no proof rejection, no `ERROR` status and no `"certified": false` record.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (one record per unit), `lane.log.tail`.
