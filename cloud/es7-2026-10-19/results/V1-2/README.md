# V1-2: sound re-check of the mirror sub-case (i) leaves with i mod 4 == 2

Instance `hm33k7.sub.cnf`, leaves from `verify/hull_leaves.icnf`; this shard takes the lines with
0-based index i, i % 4 == 2 (299 leaves).

## Tools (`tools.txt`)
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1)
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`; example prints `s VERIFIED UNSAT`)
- drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 `lrat-check.c` with `results/E2/tools/lrat-check-E2.patch`:
  it rejects the forged proof `2 0 0` on `p cnf 1 1 / 1 0` (`c NOT VERIFIED`, exit 1) and accepts a genuine
  CaDiCaL LRAT proof (`c VERIFIED`).

## Inputs
- `hm33k7.sub.cnf` regenerated with `results/C/scripts/make_cnfs.sh`:
  sha256 bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d (matches).
- `verify/hull_leaves.icnf`: sha256 cc11270a57ebe85ad1d5c83b15da0a3439521cc7ebd50432f16c223a1b2478b6 (matches).

## Method (`scripts/run_leaves.py`)
For each leaf cube c: cubeCnf exactly as `results/H3/scripts/check_cubes.sh` (header clause count + |c|,
unit clauses appended); `cadical -q --elim=0 --lrat --binary=false` with no time limit; the proof is
checked by cake_lpr (must print `s VERIFIED UNSAT`) and by the patched lrat-check (must print
`c VERIFIED`); then the CNF and proof are deleted. 4 leaves in parallel. One JSON line per leaf in
`leaves_cake.jsonl` (`i` = 0-based line index, cube, solver exit, times, proof bytes, both verdicts and
exit codes, child CPU seconds). Resumable: verified leaves are skipped on restart.

## Result
| | count |
|---|---|
| leaves assigned | 299 |
| solver exit 20 (UNSAT) | 299 |
| cake_lpr `s VERIFIED UNSAT` | 299 |
| patched lrat-check `c VERIFIED` | 299 |
| failures / re-solves | 0 |
| SAT | 0 |

The cube of every record equals line i of `hull_leaves.icnf`; the 299 indices are exactly
{i : i % 4 == 2}. Total CPU 8336 s (2.32 h): solve 6981 s, cake_lpr 1305 s, lrat-check 168 s
(wall-clock sums); longest solve 285 s; 7.04 GB of LRAT proofs checked and deleted. Wall time
about 36 min on 4 cores (`env.txt`).
