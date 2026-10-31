# Task V1-0: sound LRAT re-check of hull leaves, shard i mod 4 == 0

This task re-checks the leaves of the mirror sub-case (i) instance `hm33k7.sub.cnf` whose
0-based line index i in `verify/hull_leaves.icnf` satisfies i mod 4 == 0 (300 of 1,198).
The checks use two sound LRAT checkers. The shard runs Mi-0..3 checked these leaves with
drat-trim's `lrat-check` at 2e3b2dc, and E2 showed that build to be unsound.

**Result: all 300 leaves are UNSAT. `cake_lpr` printed `s VERIFIED UNSAT` for all 300, and
the E2-patched `lrat-check` printed `c VERIFIED` for all 300. There were no SAT leaves, no
checker rejections and no re-solves.**

This is a claim about one CNF and these 300 cubes. The other three residues are separate
tasks.

## Where it ran

One cloud VM: 4 cores, 15 GB RAM, Linux 6.18 x86_64 (`env.txt`). The leaf run started at
about 04:50 UTC and ended at 05:17 UTC on 20 Oct 2026, with 4 leaves in parallel.

## Tools (`tools.txt`)

- CaDiCaL 3.0.1, `c60730422e758ef1cebe7aeddf2dda31c996bf04`.
- cake_lpr, `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa` (built with `make cake_lpr`).
- drat-trim, `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Its `lrat-check.c` was patched with
  `results/E2/tools/lrat-check-E2.patch` and built with `gcc -O2`.

Checker controls (`logs/checker_controls.log`):

| test | patched lrat-check | unpatched lrat-check | cake_lpr |
|---|---|---|---|
| cake_lpr bundled `example.cnf`/`example.lpr` | – | – | `s VERIFIED UNSAT` |
| forged `2 0 0` on `p cnf 1 1` / `1 0` | `c NOT VERIFIED` (exit 1) | `c VERIFIED` (unsound) | `c Checking failed ...` |
| genuine CaDiCaL proof, PHP(4,3) | `c VERIFIED` | – | `s VERIFIED UNSAT` |

`cake_lpr` exits 0 even when a check fails, so verdicts here come only from its output line.

## Inputs (`logs/sha256.txt`)

- `results/C/scripts/make_cnfs.sh` regenerated `hm33k7.sub.cnf` (`logs/make_cnfs.log`). Its
  sha256 is `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d`, as
  expected; it has 47,002 variables and 535,454 clauses.
- `verify/hull_leaves.icnf` has sha256
  `cc11270a57ebe85ad1d5c83b15da0a3439521cc7ebd50432f16c223a1b2478b6`, as expected.

## Method (`scripts/run_leaves.py`)

For each leaf c, the script does the following:
1. It builds cubeCnf as `results/H3/scripts/check_cubes.sh` does: the header clause count
   plus |c|, the CNF body unchanged, and one unit clause per cube literal.
2. It runs `cadical --elim=0 --lrat --binary=false` with no time limit.
3. It checks the textual LRAT proof with `cake_lpr`, then with the patched `lrat-check`.
4. It deletes the CNF and the proof.

The `ok` field is true only if both checkers accept. I checked separately that the recorded
cubes equal lines i of `hull_leaves.icnf`, and that the indices are exactly
{0, 4, …, 1196}.

`leaves_cake.jsonl` has one record per leaf with these fields:
- `i` and `cube`;
- `solver_exit`, `solve_s` and `solve_cpu_s`;
- `proof_bytes`;
- `cake_lpr`, `cake_exit`, `cake_s` and `cake_cpu_s`;
- `lrat_check`, `lrat_exit`, `lrat_s` and `lrat_cpu_s`;
- `ok`.

## Counts

| assigned | solver exit 20 | cake_lpr VERIFIED UNSAT | patched lrat-check VERIFIED | failures | SAT |
|---|---|---|---|---|---|
| 300 | 300 | 300 | 300 | 0 | 0 |

## Costs

| step | CPU time | notes |
|---|---|---|
| CaDiCaL | 4,983.8 s | longest leaf 280.3 s |
| cake_lpr | 1,060.8 s | longest leaf 23.1 s |
| patched lrat-check | 128.1 s | |
| total | 6,172.7 s (1.71 h) | |

The proofs total 5.90 GB; the largest is 188.7 MB. All proofs were deleted after checking.
