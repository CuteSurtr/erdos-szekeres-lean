# WAVE3 / G1: open cubes of U_L2

Cloud VM with 4 cores and 15 GB RAM (`env.txt`). Run from 11:18 to 14:06 UTC on 2026-10-20. Tools are listed in `tools.txt`:
CaDiCaL 3.0.1 c6073042, march_cu 705b60c6 built with `-fcommon`, and cake_lpr a36874a8 (its bundled example prints `s VERIFIED UNSAT`).
F was regenerated and its sha256 is 69c1dc8f…ffff932d. The case CNF U_L2 (U=[], L=[2]) was rebuilt with hullsplit.py; its sha256 1d26b947…aaa53 matches cases.jsonl.
The driver `close_march.py` is a byte copy of WAVE2/F2's driver. `driver.diff` records checks (a), (b) and (c).
It was run as `--name U_L2 --top <741 given cubes> --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.724`.

## Result per case

| case | cubes given | verified leaves | open cubes left | given cubes fully covered | covered? |
|---|---|---|---|---|---|
| U_L2 | 741 | 1129 | 1937 | 709 / 741 | **no** |

- The 32 given cubes that are not yet covered:
  - 31 were split once (64 sub-cubes each) and are only partly closed;
  - 1 was never attempted.
- `open.icnf` lists exactly the 1937 frontier cubes still open: the unclosed sub-cubes of split cubes, plus the given cube that was not attempted.
- `open.icnf` was recomputed independently from `leaves.jsonl`, and it matches.
- Each line of `leaves.icnf` is a full cube over F's variables (the given cube plus the split literals). Every leaf has a `leaves.jsonl` record with `cake_lpr: "s VERIFIED UNSAT"`.
- Records: 1129 UNSAT (all verified by cake_lpr), 37 SPLIT, 0 TIMEOUT, 0 SAT.
- Time, summed over jobs:
  - CaDiCaL solve 29,188 s;
  - cake_lpr check 3,684 s;
  - march_cu split 5,155 s.

**No SAT result. No cake_lpr rejection** (every UNSAT proof printed `s VERIFIED UNSAT` on the first try).

## Incident (no effect on results)
At about 11:45 a `git pull --rebase` in the working checkout swapped out `U_L2/leaves.jsonl` while the driver was running. As a result, records the driver appended afterwards landed in a file that held only the 3 header lines.
- Repair: I joined the committed copy (34 lines, commit ccd67526) with the records that came after it.
- Checks: there are no duplicate cubes, and the frontier rebuilt from the merged file equals the driver's final `open.icnf`.
- The driver keeps its state in memory and appends to `leaves.jsonl`, so it was not affected.
- After that, commits were made from a separate clone using snapshots of the output.
