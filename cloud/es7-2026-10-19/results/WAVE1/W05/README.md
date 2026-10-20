# W05: U_L2, shard 5 of 12 (wave 1, mirror sub-case (ii))

**Result: CLOSED.** All 11 top cubes of shard 5 are refuted. The refutation uses 704 leaves, and each leaf has a cake_lpr `s VERIFIED UNSAT`. `open.icnf` is empty. No SAT answers.

## Machine and tools
- `env.txt`: Linux x86_64, 4 cores, 15 GB RAM, cloud session started 2026-10-20 06:56 UTC.
- `tools.txt`:
  - CaDiCaL 3.0.1, c60730422e75;
  - march_cu from CnC 705b60c6, built with `-fcommon`;
  - cake_lpr a36874a8. Its bundled example gives `s VERIFIED UNSAT`.
- No proof was checked with drat-trim lrat-check.

## sha256 checks (`hashes.txt`), all OK
| file | sha256 | |
|---|---|---|
| base `m33k7int.sub.cnf` (regenerated with `results/C/scripts/make_cnfs.sh`) | 69c1dc8f…932d | matches |
| `verify/ii_wave1.json` | 6df36dab…c72e | matches |
| `results/Mii-S/cases.jsonl` | bf77e23c…6f58 | = value in ii_wave1.json |
| case U_L2 (`hullsplit.py case BASE "" 2`) | 1d26b947…aa53 | matches entry |
| `U_L2.s5/top.icnf` (`march_cu -d 7`) | f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd | 128 cubes, 0 refuted. Same hash as the other U_L2 shards that had reported by 07:03 UTC (W00–W04, W06, W08–W10) |

## Method
- `scripts/close_march_shard.py` is a variant of `results/Mii-S/scripts/close_march.py`. An unchanged copy of the original is in `scripts/`.
- Changes from the original:
  - `--top` reuses the shared top-cube file;
  - `--shard 5 --nshards 12` keeps the cubes with line index i, i mod 12 == 5;
  - the run is resumable: SPLIT records list their `subs`, and only records with cake_lpr `s VERIFIED UNSAT` count as closed;
  - SAT answers are stored as a witness, not as a CNF;
  - `open.icnf` is written at the end;
  - the log is kept outside the git tree.
- Settings: 4 jobs, CaDiCaL `--lrat -t 300`, `march_cu -d 6` on timeout, cake_lpr on every UNSAT.
- Top cube indices: 5, 17, 29, 41, 53, 65, 77, 89, 101, 113, 125.
- All 11 top cubes timed out at 300 s. Each was split by `march_cu -d 6` into 64 cubes (0 refuted), which gives 704 leaves of depth 13. All 704 leaves came back UNSAT with cake_lpr `s VERIFIED UNSAT`.

## Numbers
- Leaf solve time:
  - median 21.7 s, max 244.9 s.
- LRAT proofs:
  - 19.4 GB in total, largest 170 MB;
  - deleted after checking.
- CPU time, as the sum of per-job wall time for single-threaded jobs:
  - CaDiCaL 5.82 h;
  - cake_lpr 0.85 h;
  - march splits 0.22 h;
  - top march 0.05 h;
  - total about 6.9 core-h. Wall time 07:19–09:06 UTC.
- The `child_cpu_s` field in the records is process-wide, so it over-counts. Ignore it.
- One aborted first attempt cost about 1 core-h (07:03–07:19). Its log was not kept.

## Cover (`U_L2.s5/covercheck.txt`)
`covercheck.py`:
- leaves.icnf plus the other 117 top cubes: `s COVERED`;
- each of the 11 own top cubes against its 64 leaves: `s COVERED`.

## Incident
- The periodic committer ran `git pull --rebase --autostash`. This replaced `leaves.jsonl` while the solver held it open, so records went to a deleted inode.
- Run 1 (07:19–08:06): every record (267 lines) was recovered from `/proc/<pid>/fd`.
- Aborted first attempt (07:03–07:19): its records were lost. That attempt was discarded and redone.
- The script now writes its live log in the scratchpad (`--log`), and the committer copies it into the tree.
