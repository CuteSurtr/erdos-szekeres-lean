# WAVE3 G26: open cubes of U3_L13 and U3_L5

Task: `results/WAVE3/tasks/G26.json` (commit 40e11ae). Environment in `env.txt` (4 cores, 15 GB);
tools and hashes in `tools.txt`; driver review in `driver.diff`.

F.cnf was regenerated (sha256 69c1dc8f…ffff932d, matches). Both case CNFs were built with
`hullsplit.py case` and their sha256 match `cases.jsonl`. The given cubes were written in file order
to `<case>/top.icnf` and run with `close_march.py --name <case> --top <file> --depth 7 --timeout 300
--split-depth 6` (U3_L13 with 3 jobs, U3_L5 with 1 job; after U3_L13 finished, the U3_L5 driver
was stopped and resumed with 4 jobs, and the cube that was in flight was solved again from scratch).

| case | cubes given | verified leaves | open | every given cube covered | CaDiCaL time (sum / max) | cake_lpr time (sum) |
|---|---|---|---|---|---|---|
| U3_L13 | 127 | 127 | 0 | yes: CLOSED | 771 s / 75 s | 457 s |
| U3_L5  | 58  | 58  | 0 | yes: CLOSED | 1704 s / 244 s | 391 s |

- Each given cube was solved directly (no cube hit the 300 s cap, so nothing was split); `leaves.icnf`
  equals the given cube list exactly (as sets) for both cases.
- Every leaf has cake_lpr output exactly `s VERIFIED UNSAT`. No SAT result, no cake_lpr rejection,
  no UNSAT_UNCHECKED record.
- First record of each `leaves.jsonl` carries `case` and `case_sha256`.
- Wall time: 11:20–11:40 UTC on 2026-10-20.
