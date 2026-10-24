# W26: wave 1 of mirror sub-case (ii), entry kind "cases"

Machine: 4 cores, 15 GB (env.txt). Run 2026-10-20 06:56-10:40 UTC.

## Tools
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (master at clone time)
- march_cu from CnC 705b60c6491ef2b61988b3ce6ac674be1b90571d (built with -O3 -fcommon)
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`; bundled example prints `s VERIFIED UNSAT`)

## Hash checks (all match)
- m33k7int.sub.cnf regenerated (gen_etv.py + mirgen.py, as make_cnfs.sh): 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d
- verify/ii_wave1.json: 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e
- case CNFs (hullsplit.py case): U14_L 5a99373c…e35e3, U7_L d320d668…11d3cb, U_L10 4614d05f…864081, U13_L 23571e1f…92b1 (full hashes in each leaves.jsonl "case_sha256")

## Method
`scripts/close_march.py` = results/Mii-S/scripts/close_march.py (copy in close_march_orig.py) plus: resume from
leaves.jsonl/top.icnf, `--whole T` (plain CaDiCaL on the whole case first, accepted only with cake_lpr),
`--shard/--nshards`, SPLIT records store their children, leaves.icnf only lists cake_lpr `s VERIFIED UNSAT`
leaves, open.icnf lists the cubes left. Parameters: whole 60 s, march_cu -d 7 top, CaDiCaL -t 300, march_cu -d 6 splits.
Every UNSAT was checked by cake_lpr; no other checker was used. `scripts/replay_open.py` rebuilds open.icnf from the
records (used for U7_L, whose run hit a tuple bug in the final open.icnf write, fixed afterwards in close_march.py).

Streams: U14_L (2 jobs) in parallel with U7_L (2 jobs); after U14_L closed, U_L10 then U13_L on the free 2 cores;
U7_L restarted with 4 jobs at 10:05 (resume). Deadline for new cubes 10:30 UTC.

Note: the first 30 min of solving (07:00-07:30) were lost: a `git pull --rebase` in the run checkout replaced
leaves.jsonl under the running process. Those cubes were re-solved; later commits were made from a separate clone.

## Results
The plain 60 s CaDiCaL attempt was UNKNOWN for all four cases.

| case | top cubes | top.icnf sha256 | splits | verified leaves | other UNSAT | open | SAT | solve s | check s | march s | max proof MB |
|---|---|---|---|---|---|---|---|---|---|---|---|
| U14_L | 128 | `87d48e1dba08f71d…` | 0 | 128 | 0 | 0 | 0 | 4526 | 643 | 253 | 168 |
| U7_L | 128 | `5ce594610376ec1d…` | 11 | 665 | 0 | 143 | 0 | 18930 | 2291 | 1921 | 235 |
| U_L10 | 128 | `c5d97f141552b2aa…` | 0 | 128 | 0 | 0 | 0 | 3184 | 457 | 315 | 212 |
| U13_L | 128 | `9a6abee557c788f1…` | 0 | 128 | 0 | 0 | 0 | 4772 | 567 | 244 | 188 |

CPU: U14_L 1.51 core-h, U7_L 6.43, U_L10 1.10, U13_L 1.55 (solve + check + march).

top.icnf sha256: U14_L 87d48e1dba08f71d2c8280e1a606282942bb8390aa84c2d92f96cedaa98da9c1,
U7_L 5ce594610376ec1da0924b55e5c4eedbc2ecbebea0b7ed1a983e4c018497f144,
U_L10 c5d97f141552b2aa047f6ab0f036afac911fe51589dd9428b0588821e14829d3,
U13_L 9a6abee557c788f13aa6fe0400362155cec72c68f979c8f8c4501e2f9c114e3d (128 cubes each, 0 refuted).

## Per case (covercheck.py)
- U14_L CLOSED: leaves.icnf (128 leaves, all cake_lpr verified) `s COVERED 128`. CNF sha256 5a99373c54fad1976db3f9e38d52c4cb556a794dfb25ebd22b355f9ee84e35e3.
- U_L10 CLOSED: `s COVERED 128`. CNF sha256 4614d05f1edcfabfcc3b18a510de7fb1d1c3acd40b438c60bef0eedcb5864081.
- U13_L CLOSED: `s COVERED 128`. CNF sha256 23571e1f143e3b493caa96483513be1a972084fb75dab51928cf47bb4faf32b1.
- U7_L OPEN: 665 verified leaves, 143 open cubes (open.icnf: 128 of length 19, 3 of 24, 12 of 25);
  leaves.icnf alone `s NOT COVERED`; leaves.icnf + open.icnf `s COVERED 808`. Resume with
  `close_march.py U7_L.cnf U7_L --jobs 4` (picks up top.icnf and leaves.jsonl).

No SAT answer in any run.
