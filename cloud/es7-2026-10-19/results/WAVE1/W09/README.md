# W09 — wave 1, sub-case (ii): U_L2 shard 9 of 12 — CLOSED

Machine: cloud VM, 4 cores, 15 GB RAM (`env.txt`). Run 2026-10-20 06:56–08:22 UTC.

## Tools
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1)
- march_cu, CnC 705b60c6491ef2b61988b3ce6ac674be1b90571d, built with `-O3 -fcommon`
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`; bundled example: `s VERIFIED UNSAT`)

## Hash checks (`hashes.md`)
- m33k7int.sub.cnf regenerated with results/C/scripts/make_cnfs.sh: 69c1dc8f…ffff932d — matches
- verify/ii_wave1.json: 6df36dab…00901c72e — matches
- U_L2 case CNF (`hullsplit.py case BASE "" 2`): 1d26b947…f15aaa53 — matches the entry
- top cubes `U_L2_top.icnf` (`march_cu U_L2.cnf -d 7`): **f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd**,
  128 cubes, 0 refuted, 159 s; covercheck.py on it: s COVERED 128. Other U_L2 shards must get the same sha256.

## Method
`scripts/close_march.py` is the Mii-S script (copy kept as `close_march_orig.py`) with `--top`, `--shard/--nshards`,
resume from leaves.jsonl (SPLIT records now store their children), and leaves.icnf restricted to
records with cake_lpr exactly `s VERIFIED UNSAT`. Shard 9 = top-cube lines 9, 21, …, 117 (0-based), 10 cubes.
Each cube: `cadical --lrat -t 300`; UNSAT → cake_lpr; timeout → `march_cu -d 6` split.

## Result: U_L2 shard 9 CLOSED
- All 10 top cubes timed out at 300 s and were split into 64 children each (640 children).
- All 640 children: CaDiCaL UNSAT, cake_lpr `s VERIFIED UNSAT` (640/640). No SAT. `open.icnf` empty.
- Cover: for each of the 10 top cubes T, the leaves extending T (with T stripped) give
  covercheck.py `s COVERED 64` (`U_L2.s9/covercheck.txt`); all 640 leaves lie under shard cubes.
- Leaf depth 7 + 6 = 13 literals (relative to the case CNF).
- CPU time: CaDiCaL on leaves 12,176 s (mean 19 s, max 42 s); cake_lpr 2,801 s; timed-out CaDiCaL on the 10 top
  cubes 3,000 s; march_cu splits 687 s; top march 159 s. Total ≈ 18,800 s ≈ 5.2 core-h (estimate was 14.8).
  Plus about 4 × 1–5 min of solves lost at a restart (below).
- LRAT proofs total 16.9 GB (max 138 MB), each deleted after checking.

## Incident
The first run wrote leaves.jsonl inside the git tree; the `git pull --rebase` in the push step replaced the file,
and the runner kept writing to the unlinked inode. At 07:28 the log was recovered from /proc/<pid>/fd and the runner was
restarted with resume from that log in a directory outside the repo, so no verified record was lost. The 4 solves running
at that moment were redone. The committed `U_L2.s9/leaves.jsonl` is a byte-for-byte copy of the final run log.
