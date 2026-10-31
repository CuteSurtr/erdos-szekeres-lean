# W19: wave 1, mirror sub-case (ii), U_L11 shard 0 of 4

Entry from `verify/ii_wave1.json`: kind "shard", case U_L11 (U = {}, L = {11}), shard 0 of 4.

**Result: CLOSED.** All 32 of this shard's top cubes are UNSAT, and cake_lpr printed `s VERIFIED UNSAT` for each one. No cube needed a split. Nothing is open, and no solver returned SAT.

## Environment and tools
- One cloud VM: Linux x86_64, 4 cores, 15 GB RAM (`env.txt`).
- Tools are listed in `tools.txt`: cadical c6073042, CnC/march_cu 705b60c6 (built with -fcommon), cake_lpr a36874a8. The bundled cake_lpr example prints `s VERIFIED UNSAT`.
- Proofs were checked only with cake_lpr, never with drat-trim lrat-check.

## Hash checks (`hashes.txt`)
- The regenerated base `m33k7int.sub.cnf` has sha256 69c1dc8f…932d. Match.
- `verify/ii_wave1.json` has sha256 6df36dab…e72e. Match.
- The U_L11 case CNF (`hullsplit.py case BASE "" 11`) has sha256 add0c4d2…fe504. This matches the entry.
- Top cubes: `march_cu U_L11.cnf -d 7 -o top.icnf` took 222 s and gave 128 cubes, 0 of them refuted, with sha256 55715882b809a8c9c4d39f379560b93da7f6c233cedcd0ec8fa321dde8058f06. The shards on W20, W21 and W22 recorded the same sha256 in their leaves.jsonl.

## Run
- The script is `scripts/close_march.py`, a copy of `results/Mii-S/scripts/close_march.py` with these changes (the unchanged original is in `close_march_orig.py`):
  - new `--shard`/`--nshards` options;
  - resume from leaves.jsonl, with sub-cubes stored in SPLIT records;
  - a deadline;
  - a leaf counts only when cake_lpr prints `s VERIFIED UNSAT`;
  - `open.icnf` is written;
  - solver output is kept for SAT answers.
- The command was `--depth 7 --timeout 300 --split-depth 6 --jobs 4 --shard 0 --nshards 4`. The shard takes the top cubes at 0-based line index i with i mod 4 == 0, which gives 32 cubes.
- Wall time was 07:04:17 to 07:09:07 UTC on 2026-10-20, under 5 minutes.
- Per-leaf CaDiCaL time added up to 806 s; the slowest leaf took 45.6 s.
- cake_lpr time added up to 236 s; the slowest check took 12.8 s.
- Total text LRAT was 0.94 GB. Proofs were deleted after checking.
- The `cpu_s` field in the records overcounts. It is a process-wide children delta, so with 4 threads it also counts other threads' work. Use solve_s + check_s instead: about 0.29 core-hours, plus 222 s for the top march.
- The estimate in ii_wave1.json was 13.7 core-hours, so it was far too pessimistic for this shard.

## Files (`U_L11_s0of4/`)
- `top.icnf`: the 128 top cubes, identical on all 4 shards.
- `march_top.log`: the march_cu log for the top cubes.
- `leaves.jsonl`: all records.
- `leaves.icnf`: the 32 verified leaves (sha256 6463a66a…e6e0). As a set, these are exactly this shard's 32 top cubes.
- `open.icnf`: empty.
- `covercheck.txt`: output of `results/Mii-S/scripts/covercheck.py leaves.icnf + the other 96 top cubes`, which is `s COVERED 128`. The other 96 cubes alone give `s NOT COVERED` (control). The whole top.icnf gives `s COVERED`, so top.icnf is a partition. Together these show that the verified leaves cover this shard's part of U_L11.
