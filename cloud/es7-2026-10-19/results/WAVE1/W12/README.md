# W12, wave 1: U_L4, shard 0 of 3: CLOSED

Entry in `verify/ii_wave1.json`: `{"kind": "shard", "case": "U_L4", "shard": 0, "nshards": 3, "est_core_h": 12.9}`.

## Machine and tools
- Cloud container, 4 cores, 15 GB RAM (`env.txt`). Run on 2026-10-20 from 06:56 to 08:45 UTC.
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1). march_cu from CnC 705b60c6, built with
  `-fcommon`. cake_lpr a36874a8 (`make cake_lpr`); its bundled example prints `s VERIFIED UNSAT`.
  The details are in `checks.md`.
- No proof was checked with drat-trim's lrat-check. Every leaf counted here has cake_lpr `s VERIFIED UNSAT`.

## Hash checks (all match)
| object | sha256 |
|---|---|
| base `m33k7int.sub.cnf` (regenerated: gen_etv.py + mirgen.py, as in make_cnfs.sh) | 69c1dc8f…932d |
| `verify/ii_wave1.json` | 6df36dab…c72e |
| `results/Mii-S/cases.jsonl` | bf77e23c…6f58 |
| case `U_L4` (`hullsplit.py case BASE "" 4`) | eb730ad3eebdd96f8daf71efb79c4932d861ddd0e0b1c8b38c6423112bf66df8 |
| `U_L4_s0/top.icnf` (`march_cu U_L4.cnf -d 7`) | **c172b9354496170c210bab5707ff63b120495823df0ac3b38b04da125cbfcd08** |

Top cubes: 128 cubes, including 0 refuted leaves (233.5 s). `covercheck.py top.icnf`: `s COVERED 128`.
The other U_L4 shards (W13 and W14 if the assignment is sequential) must record the same top.icnf sha256.

## Method
`scripts/close_march.py` is a copy of `results/Mii-S/scripts/close_march.py` (commit 3431b63, unchanged)
with these changes: `--top` (reuse top.icnf), `--shard/--nshards` (cube-line index i, i mod 3 == 0,
so 43 roots), resume from leaves.jsonl (SPLIT records now store their children), `leaves.icnf` restricted to
cake_lpr `s VERIFIED UNSAT`, `open.icnf`, and cake_lpr stderr kept on failure. The parameters were as
specified: cadical `--lrat -t 300`, timeouts split with `march_cu -d 6`, and 4 jobs.

## Result
| | |
|---|---|
| roots (top cubes of the shard) | 43 |
| verified leaves (`leaves.icnf`) | 673 (depth 7: 41, 13: 126, 19: 123, 25: 319, 31: 64) |
| splits (each 64 children, 0 refuted) | 10 |
| open cubes (`open.icnf`) | 0 |
| cake_lpr verdicts on the leaves | 673 × `s VERIFIED UNSAT` |
| SAT | none |
| sha256 `leaves.icnf` | ac5306f3f486ecac13e4db82ea927fc0ae990a167316fac9b2a0a6795ab93d8a |
| CPU (recorded) | solve 18,535 s + cake_lpr 2,474 s + split march 1,357 s + top march 234 s ≈ 6.3 core-h |
| wall | 07:02 to 08:39 UTC |

The recorded CPU leaves out about 0.3 core-h of solver work that was lost when the run was restarted once (see below).
The largest single leaf took 282 s to solve and its LRAT proof was 0.25 GB. Proofs were deleted after checking.

Cover check: `covercheck.py U_L4_s0/leaves.icnf others.icnf` gives `s COVERED 758`. Here others.icnf holds the 85 top
cubes of shards 1 and 2, so the leaves cover exactly the shard-0 part of the top partition. As a control,
`others.icnf` alone gives `s NOT COVERED`. All 673 leaves extend a shard-0 root. covercheck.py is the
Python sanity port; the certified check is still `lake exe cover_check` (results/H3).

## Incidents
- The first launch wrote its scratch directories (`s_k/f.cnf`, `s_k/p.lrat`) and leaves.jsonl inside
  this results dir. The first progress commit (fdce47c) therefore contained four case CNFs (about 9 MB each) and
  four partial LRAT files. They were removed in the next commit, and a `.gitignore` now excludes them. The history
  was not rewritten because other machines push to the same branch.
- The rebase autostash in that push rewrote files the run had open. Two proofs that were still being
  written were truncated, and cake_lpr rejected them (empty output, recorded as `UNSAT_UNVERIFIED`).
  leaves.jsonl was replaced by a new inode. The records were recovered from the open file descriptor, and the run was
  restarted with its work dir outside the repository (/home/user/work), resuming from the records.
  Both rejected cubes were then re-solved, and their new proofs got `s VERIFIED UNSAT`. The rejected records
  stay in leaves.jsonl. cake_lpr behaved correctly here: it refused corrupted proofs.

## Files
- `U_L4_s0/leaves.jsonl`: all records (start, leaf, split, end).
- `U_L4_s0/leaves.icnf`: the 673 verified leaves, as `a lits 0`.
- `U_L4_s0/open.icnf`: empty.
- `U_L4_s0/top.icnf`: the depth-7 top cubes.
- `U_L4_s0/march_top.log`, `run2.log`.
- `checks.md`, `env.txt`, `scripts/close_march.py`.
