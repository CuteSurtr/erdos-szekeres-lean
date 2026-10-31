# Task V1-1: sound LRAT re-check of hull leaves, shard i mod 4 == 1

This task re-checks the leaves of the mirror sub-case (i) instance `hm33k7.sub.cnf` whose
0-based line index i in `verify/hull_leaves.icnf` satisfies i mod 4 == 1 (300 of 1,198:
i = 1, 5, ..., 1197). Each leaf was checked with two sound LRAT checkers.

**Result: all 300 leaves are UNSAT. CaDiCaL exited 20 on all 300. `cake_lpr` printed
`s VERIFIED UNSAT` for all 300, and the E2-patched `lrat-check` printed `c VERIFIED` for all
300. There were no SAT leaves, no checker rejections and no re-solves.**

This is a claim about one CNF and these 300 cubes. The other three residues are V1-0, V1-2
and V1-3.

## Runs

- An earlier session (`env.txt`) built the tools, recorded `tools.txt` and `sha256.txt`, and
  finished 9 leaves (lines 9, 5, 1, 21, 13, 25, 17, 37, 29) before it stopped.
- The resumed session (`env_rerun.txt`: one cloud VM, 4 cores, 15 GB RAM, Linux 6.18 x86_64)
  rebuilt all three tools at the same commits, repeated the controls and input hashes, and
  ran the other 291 leaves from 06:29 to about 06:58 UTC on 20 Oct 2026, 4 at a time. It kept
  the 9 earlier records and skipped their line indices.

## Tools (`tools.txt`, same commits in both sessions)

- CaDiCaL 3.0.1, `c60730422e758ef1cebe7aeddf2dda31c996bf04` (`./configure && make`).
- cake_lpr, `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa` (`make cake_lpr`). The bundled
  `example.cnf`/`example.lpr` printed `s VERIFIED UNSAT`.
- drat-trim, `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, with `lrat-check.c` patched by
  `results/E2/tools/lrat-check-E2.patch` (`patch lrat-check.c <file>`) and built with
  `gcc -O2`. The forged proof `2 0 0` on `p cnf 1 1` / `1 0` is rejected:
  `c FAILED: empty clause without a RUP conflict ... c NOT VERIFIED`, exit 1.

## Inputs (`sha256.txt`)

- `results/C/scripts/make_cnfs.sh` regenerated `hm33k7.sub.cnf`, sha256
  `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d` (matches).
- `verify/hull_leaves.icnf`, sha256
  `cc11270a57ebe85ad1d5c83b15da0a3439521cc7ebd50432f16c223a1b2478b6` (matches; 1,198 lines).

## Method (`scripts/run_leaves.py`)

For each leaf cube c: cubeCnf is the CNF with header clause count + |c| and one unit clause
per literal of c appended, as in `results/H3/scripts/check_cubes.sh`. It is solved with
`cadical -q --elim=0 --lrat --binary=false` with no time limit, and on exit 20 the proof is
checked by `cake_lpr` (verdict taken only from the `s VERIFIED UNSAT` line) and by the
patched `lrat-check` (needs exit 0 and a `c VERIFIED` line). CNF and proof files were deleted
after each leaf. A checker rejection would have triggered one re-solve; none occurred.

## Final check of `leaves_cake.jsonl`

- 300 records, one for each line index i ≡ 1 (mod 4) in 0..1197, no duplicates or extras.
- Every record's cube equals line i of `hull_leaves.icnf`.
- solver_exit 20: 300; cake_lpr VERIFIED UNSAT: 300; patched lrat-check VERIFIED: 300;
  failures: 0; SAT: 0; attempts > 1: 0.
- CPU time over all 300 records: solving 6,564 s, checking 1,445 s, total 8,009 s (2.22 h).
  Largest proof 254.5 MB; longest solve 347 s.
