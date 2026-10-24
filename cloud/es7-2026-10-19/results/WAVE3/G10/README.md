# WAVE3 G10: open cubes of case U_L15

Branch `es7-cloud`. Task file `results/WAVE3/tasks/G10.json` (committed at 9a26cc2): case U_L15, 64 open cubes
(each of length 7, over F's variables). Environment in `env.txt` (4 cores, 15 GB), tools and hashes in `tools.txt`,
driver check in `driver.diff`.

## Result

| case | cubes given | verified leaves | cubes still open | every given cube covered | solve / check time |
|---|---|---|---|---|---|
| U_L15 | 64 | 64 | 0 | yes: closed | 1078.8 s CaDiCaL wall (sum), 352.1 s cake_lpr (sum) |

- No SAT result. No cake_lpr rejection: all 64 proofs gave `s VERIFIED UNSAT`, and no cube needed a split
  (longest solve 54.0 s, longest check 12.0 s, largest LRAT proof 52.1 MB, not committed).
- The set of cubes in `U_L15/leaves.icnf` is exactly the set of the 64 given cubes (the order differs because
  leaves are written in completion order). `U_L15/open.icnf` is empty. `U_L15/top.icnf` is the given cubes in the
  task file's order (sha256 427f3972…).
- Wall time of the driver run: 10:58:41 to 11:04 UTC on 2026-10-20, 4 jobs.

## How it was run

1. F regenerated with `gen_etv.py 33 7 7 7 --mirror` + `mirgen.py --interior --yflip-unit`: sha256 69c1dc8f…ffff932d (matches).
2. Case CNF: `hullsplit.py case F.cnf "" "15"`: sha256 226600f0…2d8bc (matches cases.jsonl).
3. The 64 cubes written as `a l1 .. l7 0` in the file's order and passed as `--top`:
   `BIN=/opt/work/bin WORK=/opt/work/tmp python3 close_march.py U_L15.cnf U_L15 --top U_L15.top.icnf --name U_L15 --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.6`
   (`close_march.py` is a byte copy of `WAVE2/F2/close_march.py`).
4. A leaf is written to leaves.icnf only when cake_lpr printed exactly `s VERIFIED UNSAT` on its LRAT proof.

Note: the `cpu_s` field in leaves.jsonl comes from `os.times()` children totals, which are process-wide, so with
4 parallel jobs it over-counts; use `solve_s`/`check_s`.
