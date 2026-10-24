# V1R / R2: second from-scratch check of sub-case (i) leaves, shard j = 2 (i ≡ 2 mod 4)

**Result: 299 of 299 leaves verified** (CaDiCaL exit 20 and a cake_lpr output line exactly
`s VERIFIED UNSAT`). No SAT leaf, no failure, no re-run needed. No difference from the earlier
records of `results/V1-0` to `V1-3`.

Task: `results/V1R/TASK.md` at 640a56c2, with V = R2, j = 2, H = 1.5.

## Tools (`tools.txt`)
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source.
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr`; its example prints `s VERIFIED UNSAT`.

## Inputs
- `hm33k7.sub.cnf`, made with `tools/etv/gen_etv.py 33 7 7 7 --mirror --hull` then
  `results/C/scripts/mirgen.py hm33k7.cnf 33 --hull` (the `make_cnfs.sh` route, which results/H3
  shows is byte-identical to `lake exe mir_dimacs hull 33 7`): sha256
  `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d` (matches), `p cnf 47002 535454`.
- `verify/hull_leaves.icnf`: sha256 `cc11270a57ebe85ad1d5c83b15da0a3439521cc7ebd50432f16c223a1b2478b6` (matches), 1,198 lines.

## Method (own driver: `scripts/v1r_run.py`)
For each line i of `hull_leaves.icnf` with i % 4 == 2 (299 leaves), with c the literals of that line in file order:
the CNF is `p cnf 47002 (535454+|c|)`, then the body of `hm33k7.sub.cnf` unchanged, then `l 0` for each
l in c, which is how `cubeCnf (hullCnf 33 7) c` = `F ++ c.map (fun z => [z])` lists its clauses. Its sha256
is recorded. Then `cadical -q --lrat=true --no-binary CNF PROOF` (text LRAT, default options), the proof's
sha256 and size are recorded, `cake_lpr CNF PROOF` is run, and both files are deleted. 3 leaves in parallel.
`out.jsonl` has one line per leaf: i, cube, cnf_sha256, solver_exit, solve_s, proof_bytes,
proof_sha256, cake_lpr, check_s. `scripts/compare.py` compares it with the earlier records (`compare.txt`);
`run.log` is the driver log.

## Numbers
| | |
|---|---|
| leaves in share | 299 |
| CaDiCaL exit 20 | 299 |
| cake_lpr `s VERIFIED UNSAT` | 299 |
| SAT / not verified / re-runs | 0 / 0 / 0 |
| distinct CNF sha256 | 299 |
| total solve time (sum of wall times) | 8,077 s |
| total cake_lpr time (sum) | 1,542 s |
| LRAT proofs checked and deleted | 7.16 GB |
| wall time of the run | about 54 min on 4 cores (`env.txt`) |

Largest leaf: i = 754 (depth 19, cube `-1015 -525 -2045 -1979 -2030 -2014 -1421 -1997 -1825 -1960 -1940
-1919 -1897 -1850 -1874 -3006 -4641 -2706 -4337`), proof 243,187,820 bytes, solve 356.85 s (also the
slowest solve), cake_lpr 25.27 s; CNF sha256 `799cfc1f…c6f1e`, proof sha256 `889c0973…25bee`.

## Comparison with results/V1-0 to V1-3
All four earlier files index leaves 0-based (V1-1 and V1-3 call the field `line`; checked by cube equality
against `hull_leaves.icnf`). Each of the 299 indices of this share has an earlier record (from V1-2); for every
one, the cube is the same as here and as the line of `hull_leaves.icnf`, the earlier solver exit is 20 and the
earlier cake_lpr verdict is VERIFIED UNSAT. **Differences: none.** (Solve times and proof sizes differ, as
expected: V1-2 ran `--elim=0`, this run used default options; V1-2's solve total was 6,981 s.)
