# WAVE3 / G13

Task `results/WAVE3/tasks/G13.json` (at 9a26cc2): case U_L16, 64 open cubes (depth 7).

| case | cubes given | verified leaves | cubes still open | every given cube covered | solve / check time |
|---|---|---|---|---|---|
| U_L16 | 64 | 64 | 0 | yes (closed) | 1587.9 s CaDiCaL wall (sum over jobs), 373.3 s cake_lpr; about 11 min wall on 4 cores |

- No cube needed a split. Each of the 64 given cubes is itself a leaf. The longest solve took 159 s, under the 300 s cap.
- No SAT result. No cake_lpr rejection: all 64 records have `cake_lpr: "s VERIFIED UNSAT"`.
- Case CNF sha256 edd50c27…1c9a matches cases.jsonl. F sha256 69c1dc8f…932d matches.
- `U_L16/top.icnf` is the given cube list in file order (sha256 4eace48f…17ab). `leaves.icnf` has the same 64 cubes. `open.icnf` is empty.
- Tools and commits: `tools.txt`. Driver: an unmodified copy of `results/WAVE2/F2/close_march.py`. What I checked is in `driver.diff`.

## Incident during the run (no effect on the results)
In the first minute the driver wrote straight into the repo directory. The first `git pull --rebase --autostash` stashed
two verified records that the driver had just appended, and the autostash then failed to re-apply. I stopped the driver
and copied the output directory to `/opt/work/out/U_L16`. I appended the two stashed records, both
`s VERIFIED UNSAT`, back to `leaves.jsonl`. Then I restarted the driver, which resumed from `leaves.jsonl`.
From then on, commits were snapshots copied into the repo. Each cube has exactly one record, and no cube is duplicated.
Cubes that were in flight when I killed the driver were simply re-solved.
