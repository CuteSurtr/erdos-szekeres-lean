# WAVE1 / W03: U_L2, top-cube shard 3 of 12: partly closed, 540 cubes open

Entry from `verify/ii_wave1.json`: kind "shard", case U_L2 (U = [], L = [2]), shard 3, nshards 12,
est. 14.8 core-h. Run on one cloud VM (4 cores, 15 GB, Linux 6.18; `env.txt`), 2026-10-20, 06:56-10:22 UTC.

## Tools (`tools.txt`)
- CaDiCaL c6073042 (3.0.1); march_cu from CnC 705b60c6 (built with -fcommon); cake_lpr a36874a8
  (`make cake_lpr`; the bundled example prints `s VERIFIED UNSAT`).
- Proofs were checked only with cake_lpr. drat-trim lrat-check was not used.

## sha256 checks (all OK)
- base `m33k7int.sub.cnf`, regenerated with `results/C/scripts/make_cnfs.sh`: `69c1dc8f…932d`
- `verify/ii_wave1.json`: `6df36dab…c72e`
- U_L2 case CNF (`hullsplit.py case BASE "" "2"`, p cnf 47002 515182): `1d26b947…aa53`, which matches the entry
- `U_L2_s3of12/top.icnf` = `march_cu U_L2.cnf -d 7`: **`f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd`**,
  128 cubes, 0 of them refuted, 167 s. Every shard of U_L2 should have this same hash.

## Method
`scripts/close_march.py` is a copy of `results/Mii-S/scripts/close_march.py` with these changes:
`--top` (reuse top.icnf), `--shard/--nshards` (top-cube line index i with i mod 12 == 3, which gives 11 cubes),
`--work` (scratch dir outside the repo), `--deadline`, resume from leaves.jsonl, children recorded in SPLIT
records (`subs`), and exception logging. The recipe is unchanged: cadical `--lrat -t 300` on each cube.
A timeout is split with `march_cu -d 6` on CASE+cube. Every UNSAT is checked with cake_lpr. A leaf goes
into `leaves.icnf` only when cake_lpr prints `s VERIFIED UNSAT`. No new solve was started after 10:15 UTC.
Cubes left in the queue then were recorded as OPEN (`reason: deadline`) and written to `open.icnf`.

## Result
- 1034 leaves closed, all `s VERIFIED UNSAT` by cake_lpr (cake_lpr reported no failure). 25 SPLIT nodes.
  540 cubes open. **No SAT.**
- Leaf depths: 502 at depth 13, 12 at 18, 520 at 19. Open depths: 192 at 13, 92 at 19, 256 at 25.
- Compute: 11.95 core-h, summed over cubes as solve + cake_lpr check + split wall time (cake_lpr took 1.2 h of that;
  the largest proof was 237 MB). About 1 more core-h was lost in two aborted starts (see below).
  Note: the `cpu_s` field in the records counts all child processes that finished in the window, across
  threads, so it over-counts. Do not use it.
- Cover check (`scripts/shard_cover.sh`, which runs `results/Mii-S/scripts/covercheck.py`; output in `U_L2_s3of12/covercheck.txt`):
  - top.icnf alone: COVERED (128 cubes).
  - leaves.icnf + the 117 other top cubes: NOT COVERED, as expected while cubes are open.
  - leaves.icnf + open.icnf + the other top cubes: COVERED. So open.icnf is exactly what remains of this shard.

Per top cube (0-based line index in top.icnf):

| idx | top cube | cake leaves | open | |
|---|---|---|---|---|
| 3 | -987 -1420 1651 -1635 1446 1618 1581 | 64 | 0 | closed |
| 15 | -987 -1420 1651 1635 1618 1581 1600 | 127 | 0 | closed |
| 27 | -987 -1420 -1651 -1446 1471 -1635 -1600 | 127 | 0 | closed |
| 39 | -987 1420 -1651 -1446 -1635 -1600 -1618 | 190 | 0 | closed |
| 51 | -987 1420 1651 -1446 -1635 1618 1600 | 64 | 0 | closed |
| 63 | -987 1420 1651 1446 1635 1618 1600 | 335 | 284 | open |
| 75 | 987 1420 -1651 -1635 1618 -1600 -1581 | 64 | 0 | closed |
| 87 | 987 1420 1651 -1446 1635 1618 1581 | 63 | 64 | open |
| 99 | 987 -1420 1651 1446 -1635 -1618 -1581 | 0 | 64 | open (split once, children not started) |
| 111 | 987 -1420 1651 -1446 -1635 -1618 -1600 | 0 | 64 | open (split once, children not started) |
| 123 | 987 -1420 -1651 -1446 1635 -1471 -1618 | 0 | 64 | open (split once, children not started) |

**Shard status: OPEN.** 6 of 11 top cubes are closed. The run can resume:
`BIN=… close_march.py U_L2.cnf DIR --top top.icnf --shard 3 --nshards 12 --jobs J --timeout 300 --split-depth 6`
on a dir holding this `leaves.jsonl`. It skips verified leaves and SPLIT nodes and re-solves the open cubes.

## Incidents
- The first two starts lost their records. `git pull --rebase --autostash` replaced `leaves.jsonl` in the repo
  with a new inode while the runner held it open. The records of the second start were recovered from
  `/proc/PID/fd`, and the runner was moved to a directory outside the repo (copied in by a sync job).
  The 4 top cubes of the first start were solved again. Nothing was certified from lost records.
- CNF and LRAT files were kept out of git (the scratch dir was deleted).

## Files
`env.txt`, `tools.txt`, `scripts/` (close_march.py, shard_cover.sh), `U_L2_s3of12/`: `top.icnf`, `top_march.log`,
`leaves.jsonl` (all records), `leaves.icnf` (1034 cake-verified leaves, `a lits 0`), `open.icnf` (540), `covercheck.txt`, `run.log`.
