# W22: U_L11 shard 3 of 4 (mirror sub-case (ii), wave 1) — CLOSED

Machine: 4 cores, 15 GB RAM, Linux 6.18 x86_64 (`env.txt`). Run 2026-10-20, 06:56–07:35 UTC.

## Tools
- CaDiCaL `c6073042` (master HEAD at clone time), `./configure && make`.
- march_cu from marijnheule/CnC `705b60c` with `CFLAGS="-O3 -fno-strict-aliasing -Wall -DNDEBUG -fcommon"`.
- cake_lpr `a36874a`, `make cake_lpr`; bundled example prints `s VERIFIED UNSAT`.

## Hash checks (all match)
- regenerated base `m33k7int.sub.cnf` (`gen_etv.py 33 7 7 7 --mirror` + `mirgen.py --interior --yflip-unit`):
  `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`
- `verify/ii_wave1.json`: `6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e`
- case CNF `U_L11` (`hullsplit.py case BASE "" 11`): `add0c4d2d19966cf28ae3bc622c55554cefc45b04e7278c7121de4e1910fe504`
  (= entry and cases.jsonl)

## Run
`scripts/close_march.py` is `results/Mii-S/scripts/close_march.py` plus: `--shard/--nshards`, top cubes
saved to `top.icnf` and reused, resume from `leaves.jsonl`, status UNSAT only when cake_lpr prints
`s VERIFIED UNSAT`, `subs` stored on SPLIT records, `open.icnf` written at the end, exceptions logged.
Parameters: `-d 7` top, CaDiCaL `--lrat -t 300`, `-d 6` splits, 4 jobs.

- `march_cu U_L11.cnf -d 7`: 128 cubes, 0 refuted, 207.7 s.
  `top.icnf` sha256 `55715882b809a8c9c4d39f379560b93da7f6c233cedcd0ec8fa321dde8058f06`
  (same value recorded by shards 0, 1, 2 on W19–W21). `covercheck.py top.icnf`: `s COVERED 128`.
- Shard 3 = top lines i ≡ 3 (mod 4): 32 cubes.

## Result: CLOSED
- 32/32 top cubes UNSAT directly with CaDiCaL (no splits needed), every one `s VERIFIED UNSAT` by cake_lpr.
- `leaves.icnf`: 32 leaves (sha256 `5f44d882bceef44565d54e2b87007bd88bcc6742526d8983735adbdc10581bb1`); `open.icnf` empty.
- `scripts/shardcover.py top.icnf 3 4 leaves.icnf`: `s COVERED 32/32 top cubes` (covercheck.py's cover()
  applied to each shard top cube with the leaves restricted to it).
- CPU: solve 1407.6 s, cake_lpr 215.2 s, top march 207.7 s (≈ 0.5 core-hours; max cube 209 s);
  1.43 GB of LRAT, deleted after checking. The estimate of 13.7 core-hours was far too high.
- No SAT.

## Incident
The first two launches wrote `leaves.jsonl` inside the repo; `git pull --rebase --autostash` in the
commit script replaced the file while the solver held it open, so records went to an unlinked inode
and those runs ended with no usable records (5 verified records survived and were kept). The final run
worked in `~/work/U_L11` and copied files into the repo on commit; it re-solved the other 27 cubes.
No result depends on the lost runs.
