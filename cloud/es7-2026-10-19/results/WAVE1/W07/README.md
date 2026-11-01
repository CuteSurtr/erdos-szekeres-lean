# W07: wave 1, sub-case (ii), case U_L2, shard 7 of 12

Status: **OPEN (partial)**. The shard is not closed in the 4 h budget. 5 of 11 top cubes are closed, every leaf has cake_lpr `s VERIFIED UNSAT`, and 961 cubes stay open. No SAT, and no UNSAT failed its check.

## Where it ran
One cloud VM (`env.txt`: Linux 6.18 x86_64, 4 cores, 15 GB) on 2026-10-20, 06:55–10:50 UTC.
The solve ran from 07:00 to 10:26 UTC with `--jobs 4`. Tools and hash checks are in `tools_and_hashes.md`:
- CaDiCaL c6073042;
- march_cu CnC 705b60c6 built with -fcommon;
- cake_lpr a36874a8, which verifies its bundled example.

## Hash checks (all match)
- Base `m33k7int.sub.cnf` (regenerated): `69c1dc8f…f932d`.
- `verify/ii_wave1.json`: `6df36dab…1c72e`.
- `results/Mii-S/cases.jsonl`: `bf77e23c…6f58`.
- Case CNF U_L2 (`hullsplit.py case BASE "" 2`): `1d26b947…aaa53`, as in the W07 entry.
- Top cubes, `march_cu U_L2.cnf -d 7`: 128 cubes, including 0 refuted leaves.
  - sha256 of `U_L2/top.icnf`: `f00804ef5fd21981ef094016e1d77b36fb1dc7d08a6d0b0f219afcc6d30999bd`. All shards must match it.
  - covercheck on top.icnf alone: `s COVERED 128`.

## Method
`scripts/close_march.py` is the Mii-S script with these changes; the original is kept as `close_march_orig.py`:
- adds `--top/--shard/--nshards`; this shard takes top lines i with i mod 12 == 7 (7,19,…,127);
- resumes from leaves.jsonl;
- puts in leaves.icnf only leaves whose cake_lpr check printed `s VERIFIED UNSAT`;
- stops starting new solves after `--until`, then writes open.icnf.

Each cube runs CaDiCaL `--lrat -t 300`. An UNSAT goes to cake_lpr; a timeout is split with `march_cu -d 6`, 64 sub-cubes each time. Proofs were deleted after their check.

To resume, run `close_march.py U_L2.cnf DIR --top top.icnf --shard 7 --nshards 12` with DIR holding this `leaves.jsonl`.

## Results (`U_L2/`)
- `leaves.jsonl`: 891 records (862 UNSAT verified, 29 SPLIT with stored children, plus start/end records); sha256 `584467b2…`.
- `leaves.icnf`: 862 leaves (686 of depth 13, 176 of depth 19), all `s VERIFIED UNSAT`; sha256 `86a9e1b7…`.
- `open.icnf`: 961 open cubes; sha256 `ac2e8322…`.
- CPU (wall time of single-thread runs): 49,026 s ≈ 13.6 core-h. cake_lpr took 4,616 s of that. The largest LRAT proof was 201 MB.

| top line | status | leaves | open | CPU s |
|---|---|---|---|---|
| 7 | closed | 64 | 0 | 2542 |
| 19 | closed | 64 | 0 | 1722 |
| 31 | open | 169 | 333 | 9308 |
| 43 | closed | 127 | 0 | 5218 |
| 55 | open | 63 | 64 | 4344 |
| 67 | closed | 64 | 0 | 1867 |
| 79 | open | 63 | 64 | 5310 |
| 91 | open | 63 | 64 | 4162 |
| 103 | open | 62 | 128 | 5224 |
| 115 | closed | 64 | 0 | 1864 |
| 127 | open | 59 | 308 | 7465 |

## Cover checks (`results/Mii-S/scripts/covercheck.py`)
- leaves.icnf + open.icnf + the other shards' top cubes (`others_shards.icnf`): `s COVERED 1940`. The split bookkeeping is complete.
- leaves.icnf + the top cubes other than the 5 closed ones (lines 7,19,43,67,115): `s COVERED 985`. Those 5 top cubes are closed by verified leaves.
- leaves.icnf + others_shards.icnf: `s NOT COVERED`, as expected, because the shard is still open.

## SAT
None.
