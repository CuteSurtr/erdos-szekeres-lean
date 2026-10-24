# W24 (wave 1, sub-case (ii)): U12_L, shard 1 of 2: CLOSED

Entry `{"kind": "shard", "case": "U12_L", "shard": 1, "nshards": 2, "vm": "W24"}` of `verify/ii_wave1.json`.

## Where it ran
One cloud VM, 4 cores, 15 GB RAM, Linux 6.18 x86_64 (`env.txt`). Started 06:56 UTC on 2026-10-20; the solving finished at 07:25 UTC.

## Tools (`tools.txt`)
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1), with LRAT output in text format.
- march_cu from CnC 705b60c6491ef2b61988b3ce6ac674be1b90571d, built with `-fcommon`.
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, built with `make cake_lpr`. The bundled example prints `s VERIFIED UNSAT`.

## sha256 checks (`hashes.txt`): all match
- Base CNF `m33k7int.sub.cnf`, regenerated with `results/C/scripts/make_cnfs.sh`: 69c1dc8f…f932d.
- `verify/ii_wave1.json`: 6df36dab…1c72e.
- Case CNF U12_L (`hullsplit.py case BASE 12 ""`): feb579d8…88971.

## Method
`scripts/close_march.py` is a copy of `results/Mii-S/scripts/close_march.py` with these changes:
- `--shard`/`--nshards` options;
- it can resume (it keeps `top.icnf`, and SPLIT records store their children);
- it retries cake_lpr with a larger heap if the heap runs out (this never happened here);
- it writes `open.icnf`;
- `leaves.icnf` lists only leaves with `s VERIFIED UNSAT`.

Settings: `march_cu -d 7` for the top cubes, `cadical -t 300` on each cube, `march_cu -d 6` to split a cube that times out, and cake_lpr on every UNSAT. Jobs ran 4 at a time.

## Top cubes
- `march_cu U12_L.cnf -d 7` gives 128 cubes, 0 of them refuted, in 259 s.
- sha256 of `top.icnf`: **f4ed6a255b70e082b6106b782c1239b6aeb6a40f088722940e5ac217ef155f4c**. This is the same file that W23 (shard 0) recorded.
- This shard takes the 64 cubes with 0-based line index i where i mod 2 == 1.

## Result
- **CLOSED.** 127 leaves, all with cake_lpr `s VERIFIED UNSAT`. `open.icnf` is empty. No SAT.
- One top cube timed out at 300 s: `-45532 -3765 3444 -3749 3191 -3714 -3732`. Splitting it with `-d 6` gave 64 sub-cubes (0 refuted), and all 64 are UNSAT.
- The other 63 top cubes were UNSAT directly. The slowest solve took 234 s, and the largest proof was 0.20 GB.
- CPU time, about 1.34 core-hours in all:
  - CaDiCaL 3725 s;
  - cake_lpr 706 s;
  - march splits 125 s;
  - top march 259 s.
- Not counted: the in-flight work of the first launch (about 7 min on 4 cores), which was restarted, see below.
- Cover (`U12_L_s1of2/covercheck.txt`, from `scripts/shardcover.sh` with `results/Mii-S/scripts/covercheck.py`):
  - `top.icnf` alone: COVERED (128 cubes);
  - `leaves.icnf` plus the 64 top cubes of shard 0: COVERED (191 cubes). So the verified leaves cover this shard's part.
  - Controls: shard-1 roots used as leaves gives COVERED; a partial leaf set gives NOT COVERED.
- sha256 of `leaves.icnf`: 38869ce0353bd14cd8c9e9318d7b177c6f414806bbc674d692f762b1f73ed0da.

## Incident
The first launch wrote `leaves.jsonl` inside the repo. A commit with `pull --rebase` then replaced the file while the process still had it open. I recovered the 34 records written so far (top cube record, start record, 32 UNSAT leaves with cake_lpr verdicts) from the open file descriptor, stopped that run, and resumed from those records with the live output in /tmp. Only the cubes in flight were re-run. Both start records are in `leaves.jsonl`.
