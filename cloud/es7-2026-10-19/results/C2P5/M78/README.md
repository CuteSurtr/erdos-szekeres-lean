# C2P5 M78: list C2P5B.tsv, shard j = 28 of N = 50, H = 5.25 h, task commit 81cb025f

Start 2026-10-31 15:24:33Z (epoch 1793460273), END 1793478273 (20:24:33Z). The lane ran 15:26:58Z to 19:14:09Z and finished all its units.

## Tools and checks (`tools.txt`)
- `C2P/vendor/build_tools.sh`: built from the vendored sources (manifest: all 196 files match). CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8), lrat-check (2e3b2dc + E2 patch). No code was cloned or downloaded.
- Sanity: both checkers rejected the bad LRAT and accepted the good one. The cake_lpr example printed `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`. base.cnf sha256 `b0061e90...d8ff1` and base.json sha256 `2476faff...bf472b48` both match.
- Cubes: P1..P8 from `l2cubes.py` are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (19, rows idx ≡ 28 mod 50)

| case | kind | units | certified | timed out | not reached | errors |
|---|---|---|---|---|---|---|
| P2 | Q | 1 | 1 | 0 | 0 | 0 |
| P2 | H | 6 | 6 | 0 | 0 | 0 |
| P1 | Q | 1 | 1 | 0 | 0 | 0 |
| P1 | H | 5 | 5 | 0 | 0 | 0 |
| P3 | Q | 1 | 1 | 0 | 0 | 0 |
| P3 | H | 5 | 5 | 0 | 0 | 0 |
| **total** | | **19** | **19** | 0 | 0 | 0 |

All 19 are UNSATISFIABLE. For each one, lrat-check gave `c VERIFIED` and cake_lpr gave `s VERIFIED UNSAT`, so `certified: true`.

Certified units, shown as min / median / max:

| | solve s | lrat-check s | cake_lpr s | proof GB |
|---|---|---|---|---|
| Q (3) | 458.4 / 1701.8 / 1940.3 | 57.9 / 84.7 / 89.3 | 334.3 / 457.8 / 501.5 | 3.32 / 5.14 / 5.34 |
| H (16) | 21.3 / 228.6 / 471.5 | 13.6 / 54.4 / 62.3 | 112.8 / 308.1 / 365.1 | 0.22 / 3.16 / 3.59 |
| all (19) | 21.3 / 257.0 / 1940.3 | 13.6 / 57.0 / 89.3 | 112.8 / 321.9 / 501.5 | 0.22 / 3.24 / 5.34 |

Per unit:

| unit | kind | cap s | solve s | lrat-check s | cake_lpr s | proof GB | RSS MB |
|---|---|---|---|---|---|---|---|
| P2_4-13 | Q | 8000 | 1940.3 | 89.3 | 501.5 | 5.34 | 4454.7 |
| P1_3-12 | Q | 8000 | 1701.8 | 84.7 | 457.8 | 5.14 | 4422.0 |
| P2_1-4-8 | H | 2400 | 299.4 | 57.9 | 322.2 | 3.34 | 4405.6 |
| P2_3-4-10 | H | 2400 | 93.2 | 26.5 | 177.4 | 1.19 | 3187.9 |
| P2_3-8-10 | H | 2400 | 208.6 | 52.8 | 303.6 | 3.10 | 4381.5 |
| P2_4-5-15 | H | 2400 | 345.7 | 57.0 | 328.4 | 3.40 | 4374.6 |
| P2_4-12-13 | H | 2400 | 248.7 | 56.0 | 312.6 | 3.24 | 4369.7 |
| P2_6-7-11 | H | 2400 | 81.6 | 27.0 | 172.4 | 1.18 | 3187.2 |
| P1_2-5-6 | H | 2400 | 29.1 | 13.6 | 113.3 | 0.22 | 2650.4 |
| P1_2-11-12 | H | 2400 | 312.9 | 58.9 | 321.9 | 3.30 | 4401.0 |
| P1_3-8-11 | H | 2400 | 95.3 | 28.4 | 180.9 | 1.25 | 3220.7 |
| P1_4-8-14 | H | 2400 | 357.2 | 58.7 | 352.0 | 3.35 | 4386.6 |
| P1_7-8-9 | H | 2400 | 27.4 | 13.7 | 113.3 | 0.22 | 2676.4 |
| P3_7-8 | Q | 7083* | 458.4 | 57.9 | 334.3 | 3.32 | 4358.2 |
| P3_1-6-15 | H | 2400 | 471.5 | 62.3 | 365.1 | 3.59 | 4373.0 |
| P3_1-14-15 | H | 2400 | 257.0 | 57.2 | 326.6 | 3.23 | 4397.6 |
| P3_4-9-13 | H | 2400 | 322.2 | 57.2 | 335.7 | 3.33 | 4406.9 |
| P3_5-9-10 | H | 2400 | 24.8 | 13.7 | 112.8 | 0.22 | 2678.6 |
| P3_7-8-11 | H | 2400 | 21.3 | 13.7 | 116.1 | 0.22 | 2645.5 |

\* The list cap for P3_7-8 was 8000 s. lane.py lowered it to 7083 s so that 10 minutes would remain for the checks before END. The unit finished in 458 s, so the lower cap had no effect.

## Resources and problems
- Largest solver RSS: 4454.7 MB (P2_4-13). Memory peaked at about 8 GB used, during cake_lpr, which uses an 8000 MB heap. There was no memory problem.
- Disk: the largest proof was 5.34 GB, and at least 22 GB stayed free.
- No SAT result, no proof rejection, no ERROR status, and no uncertified record.

Files: `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl` (19 records), `lane.log.tail`.
