# G21: open cubes of U_L6 (task `results/WAVE3/tasks/G21.json`, 473 cubes)

Run 2026-10-20 10:56–13:41 UTC on 4 cores (`env.txt`). Tools and hashes in `tools.txt`
(CaDiCaL 3.0.1 c6073042, march_cu 705b60c6 with `-fcommon`, cake_lpr a36874a8; its example prints
`s VERIFIED UNSAT`). F regenerated with sha256 69c1dc8f…ffff932d; the U_L6 case CNF
(`hullsplit.py case F.cnf "" "6"`) has sha256 741c7fe0…4a105424, equal to cases.jsonl.

Driver: `close_march.py`, an unchanged copy of `results/WAVE2/F2/close_march.py`; checks in
`driver.diff` (fresh mkdtemp per job, atomic leaves.icnf/open.icnf, first leaves.jsonl record has
case and case_sha256; leaves only on the exact line `s VERIFIED UNSAT`). One call:
`close_march.py U_L6.cnf U_L6 --top <473 task cubes> --name U_L6 --depth 7 --timeout 300
--split-depth 6 --jobs 4 --hours 2.6`. `U_L6/top.icnf` is the 473 task cubes in the file's order
(sha256 b08649f5…69d9b8).

## Result

| case | cubes given | verified leaves | cubes still open | every given cube covered? |
|---|---|---|---|---|
| U_L6 | 473 | 327 | 1318 | no |

- 327 of the 473 given cubes were closed directly, each by one leaf that cake_lpr verified.
- 19 given cubes timed out at 300 s and were split with march_cu (depth 6) into 1191 sub-cubes.
  None of those sub-cubes had been solved when the run stopped.
- 127 given cubes were never started.
- `open.icnf` holds 1318 = 1191 + 127 cubes. After the run I rebuilt it from leaves.jsonl with my
  own frontier walk and got the same list. leaves.icnf equals the set of records whose cake_lpr
  line is `s VERIFIED UNSAT`.
- Time: solve 17,757 s total over the 327 leaves (mean 54 s, max 284 s), check 2,343 s total
  (mean 7.2 s). The 19 timeouts cost about 64,700 CPU-s for solving and splitting.
- No SAT result, and cake_lpr rejected nothing: all 327 UNSAT proofs gave `s VERIFIED UNSAT`.

The case is **not closed**. To continue, run the driver again on the same `U_L6/` directory (it
resumes from leaves.jsonl), or hand out `open.icnf` as the next task.
