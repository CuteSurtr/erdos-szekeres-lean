# V1R / R0: second from-scratch check of sub-case (i) leaves, shard j = 0

Task: `results/V1R/TASK.md` at 640a56c2, with V = R0, j = 0, H = 1.5. Share: the 300 cubes of
`verify/hull_leaves.icnf` with 0-based line index i ≡ 0 (mod 4).

**Result: 300 of 300 leaves verified.** For each one, CaDiCaL exited 20 and cake_lpr printed a line that is exactly
`s VERIFIED UNSAT`. No leaf was SAT and none failed verification.

## Tools (`tools.txt`)
- CaDiCaL 3.0.1, git c60730422e758ef1cebe7aeddf2dda31c996bf04, `./configure && make`.
- cake_lpr, git a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr` (gcc 13.3.0). `cake_lpr.S`
  sha256 2f3af32d…72b7d4a, `basis_ffi.c` sha256 8e30d84f…. The bundled example prints `s VERIFIED UNSAT`.
- Machine: 4 cores, 15 GB RAM (`env.txt`).

## Inputs
- `hm33k7.sub.cnf` sha256 `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d`, which matches the
  expected value. Header `p cnf 47002 535454`. I generated it with the repository's Python reference path,
  the two `results/C/scripts/make_cnfs.sh` steps `tools/etv/gen_etv.py 33 7 7 7 --mirror --hull` and
  `results/C/scripts/mirgen.py hm33k7.cnf 33 --hull`. `results/H3` records that this file is byte-identical
  to the output of the Lean `lake exe mir_dimacs`. I did not build the Lean generator. The sha256 match is the check.
- `verify/hull_leaves.icnf` sha256 `cc11270a57ebe85ad1d5c83b15da0a3439521cc7ebd50432f16c223a1b2478b6`, which
  matches. It has 1,198 lines.

## Method (`scripts/`, written from scratch)
- `leaf.sh` builds each leaf CNF in the order of `cubeCnf (hullCnf 33 7) c`: the header
  `p cnf 47002 535454+|c|`, then the body of `hm33k7.sub.cnf` unchanged, then one unit clause per cube
  literal in file order. It records the CNF's sha256, then runs
  `cadical -q --lrat=true --no-binary f.cnf p.lrat` and `cake_lpr f.cnf p.lrat`. It records the proof's
  size and sha256 and then deletes the CNF and the proof.
- `run.sh` runs all 300 leaves, 3 in parallel with `xargs -P 3`. `compare.py` compares the output
  with `results/V1-0` to `V1-3`, matching records by cube. Its output is in `compare.txt`.
- `rerun.sh` covers one run problem. Nine leaves (i = 0, 4, 8, 64, 68, 72, 384, 388, 392) lost their output
  line because they were running when my `git pull --rebase --autostash` replaced `out.jsonl` while they
  had it open. Their verdicts were never seen; the records were simply lost. They were re-run in a second
  pass that wrote to scratch files first, and all 9 verified. `out.jsonl` has exactly one record per leaf,
  sorted by i.

## Numbers
- Total solve time 5,265.5 s, total check time (cake_lpr) 1,402.6 s, both wall time summed over leaves.
  Elapsed time for the whole run was about 45 min.
- Largest leaf by proof size: i = 16, proof 166,322,459 bytes, solve 215.8 s, check 20.2 s.
  Longest solve: i = 880, 249.8 s.

## Comparison with the earlier records
All 300 of my cubes are in `results/V1-0/leaves_cake.jsonl` with the same i and the same cube, and each has one
earlier record. For every leaf the solver exit (20) and the cake_lpr verdict (`s VERIFIED UNSAT`) agree.
**Differences: none** in cube, index, solver exit or verdict.

Not a difference in verdict: proof sizes match V1-0 for 185 of the 300 leaves and differ for 115. V1-0 ran
CaDiCaL with `--elim=0 --lrat --binary=false` (`results/V1-0/scripts/run_leaves.py`, line 55), and this run
used the task's `--lrat=true --no-binary`, so the proofs are not expected to be the same. V1-0 has no proof or
CNF hashes, so those cannot be compared. This run's per-leaf `cnf_sha256` and `proof_sha256` are new.
