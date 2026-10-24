# WAVE3 G7: open cubes of U16_L

Task file `results/WAVE3/tasks/G7.json` (commit 9a26cc2): U16_L, 64 cubes.
Environment in `env.txt` (4 cores, 15 GB). Tools and commits in `tools.txt`; driver check in `driver.diff`.

- F regenerated with gen_etv.py + mirgen.py: sha256 69c1dc8f…ffff932d (matches).
- U16_L case CNF from `hullsplit.py case F.cnf 16 ""`: sha256 49f74507…8e25fab4 (matches cases.jsonl).
- The 64 cubes were written in file order to `U16_L/top.icnf` and run with
  `close_march.py --name U16_L --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours 2.714`.

## Result

| case | cubes given | verified leaves | still open | every given cube covered |
|---|---|---|---|---|
| U16_L | 64 | 64 | 0 | yes (closed) |

- Every one of the 64 given cubes was proved UNSAT directly by CaDiCaL (no timeouts, no splits). cake_lpr printed
  `s VERIFIED UNSAT` on all 64 LRAT proofs.
- `leaves.icnf` is exactly the set of the 64 given cubes (checked: 64 distinct lines, each ending in ` 0`,
  set equal to G7.json). `open.icnf` is empty.
- Time: total solve 2963.5 s (max 241 s per cube), total cake_lpr check 552.0 s. Largest proof 169 MB.
  Wall time 11:20–11:36 UTC (16 min). (The `cpu_s` field in leaves.jsonl is measured process-wide via
  os.times and overcounts under concurrency.)
- No SAT results. No cake_lpr rejections.
