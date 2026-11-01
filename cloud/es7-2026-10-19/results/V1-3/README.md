# V1-3: sound re-check of the sub-case (i) leaves with line index i % 4 == 3

**Result: all 299 assigned leaves of `verify/hull_leaves.icnf` (0-based line index i, i % 4 == 3)
are UNSAT, and every proof was accepted by both cake_lpr (`s VERIFIED UNSAT`) and the
E2-patched lrat-check (`c VERIFIED`). 0 SAT, 0 checker rejections, 0 re-solves.**

This re-establishes, with sound checkers, the verdicts of this quarter of the 1,198 leaves.
It is a claim about the CNF `hm33k7.sub.cnf`; the cover of the leaves is a separate check
(see `verify/README.md`).

## Environment and tools

- Cloud VM, 4 cores, 15 GB RAM (`env.txt`). Run from 04:51 to 05:31 UTC on 20 October 2026.
- `tools.txt`: CaDiCaL c607304 (3.0.1), cake_lpr a36874a8 (`make cake_lpr`; bundled example prints
  `s VERIFIED UNSAT`), drat-trim 2e3b2dc lrat-check with `results/E2/tools/lrat-check-E2.patch`.
- The patched lrat-check rejects the forged proof `2 0 0` on `p cnf 1 1 / 1 0`
  (`c FAILED: empty clause without a RUP conflict`, `c NOT VERIFIED`, exit 1) and accepts a
  genuine CaDiCaL proof (`c VERIFIED`).

## Inputs (`setup.txt`)

- `hm33k7.sub.cnf` regenerated with `results/C/scripts/make_cnfs.sh`: `p cnf 47002 535454`,
  sha256 `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d` (matches).
- `verify/hull_leaves.icnf`: 1,198 lines, sha256
  `cc11270a57ebe85ad1d5c83b15da0a3439521cc7ebd50432f16c223a1b2478b6` (matches).

## Method (`scripts/run_leaves.py`)

For each leaf c: cubeCnf exactly as `results/H3/scripts/check_cubes.sh` (header clause count
+ |c|, unit clauses appended); `cadical -q --elim=0 --lrat --binary=false` with no time limit;
cake_lpr must exit 0 and print `s VERIFIED UNSAT`; patched lrat-check must exit 0 and print the
line `c VERIFIED`. 4 leaves in parallel; CNF and proof deleted after both checks. A rejected
proof would have been re-solved once (none was).

## Numbers (`leaves_cake.jsonl`, one line per leaf)

- Leaves assigned: 299 (depth 7: 29, 13: 159, 19: 79, 25: 32). The line indices are exactly
  {i : i % 4 == 3} and every recorded cube equals its line in `hull_leaves.icnf`.
- Solver exit 20 (UNSAT): 299. SAT: 0.
- cake_lpr `s VERIFIED UNSAT`: 299. Patched lrat-check `c VERIFIED`: 299. Failures: 0.
- Times (wall per process, summed): CaDiCaL 7,363 s (longest 349.8 s), cake_lpr 1,169 s,
  lrat-check 168 s; total 8,700 s. Child-process CPU (getrusage): 7,946 s user + 623 s sys
  = 8,570 s.
- LRAT proofs: 7.04 GB in total, largest 242 MB; all deleted after checking.
