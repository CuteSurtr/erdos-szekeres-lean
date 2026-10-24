# W20 — wave 1, sub-case (ii): U_L11, shard 1 of 4

Result: **shard 1 of U_L11 is closed.** All 32 top cubes of the shard are UNSAT with cake_lpr
`s VERIFIED UNSAT`; no split was needed, no SAT answer, `open.icnf` is empty.

## Machine
One cloud VM (4 cores, 15 GB RAM, Linux 6.18 x86_64), see `env.txt`. Run on 2026-10-20 (UTC).

## Tools (see `hashes.txt`)
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04
- march_cu (CnC 705b60c6491ef2b61988b3ce6ac674be1b90571d, built with `-O3 -fcommon`)
- cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`; bundled example: `s VERIFIED UNSAT`)

## sha256 checks (all OK)
- regenerated `m33k7int.sub.cnf`: 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d
- `verify/ii_wave1.json`: 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e
- `U_L11.cnf` (`hullsplit.py case BASE "" 11`): add0c4d2d19966cf28ae3bc622c55554cefc45b04e7278c7121de4e1910fe504 (= entry)

## Top cubes
`march_cu U_L11.cnf -d 7 -o top.icnf` (223 s): **128 cubes, 0 refuted**, sha256
`55715882b809a8c9c4d39f379560b93da7f6c233cedcd0ec8fa321dde8058f06` (copy in `U_L11_s1/top.icnf`).
All four U_L11 shards should report this sha256. covercheck.py on top.icnf alone: `s COVERED 128`.
Shard 1 = 0-based line indices i ≡ 1 (mod 4): 32 cubes.

## Run
`scripts/close_march.py` = copy of `results/Mii-S/scripts/close_march.py` (original in
`scripts/close_march.orig.py`) with `--top/--shard/--nshards`, resume from leaves.jsonl, deadline,
`--finalize` (writes leaves.icnf / open.icnf), SAT model capture. Recipe unchanged: cadical --lrat -t 300,
cake_lpr on every UNSAT, march_cu -d 6 on a timeout. `--jobs 4`.

| part | top cubes | leaves (cake_lpr verified) | splits | open | SAT | cadical CPU | cake_lpr CPU | wall |
|---|---|---|---|---|---|---|---|---|
| U_L11 shard 1/4 | 32 | 32 | 0 | 0 | 0 | 1001 s (max 140 s per cube) | 213 s | ~6 min |

LRAT proofs total 1.13 GB (text), deleted after checking. `leaves.icnf` sha256
`f965bfebeeddf03c0b12d44f65841d3cb766a9a1f5ddabae737ccd3efa8cd640`.

## Cover check
- `covercheck.py leaves.icnf + (the 96 top cubes of shards 0, 2, 3)`: `s COVERED 128`, so the leaves
  cover this shard's part of U_L11.
- leaves.icnf equals the 32 shard top cubes exactly.

## Notes
- The estimate in ii_wave1.json was 13.7 core-h for this shard; it took about 0.34 core-h (the depth-7
  cubes were all solved directly in at most 140 s).
- The first start (07:02 UTC) was restarted after ~2 min: `git pull --rebase --autostash` replaced the
  tracked leaves.jsonl while the solver held it open. The live run then wrote outside the repo and
  snapshots were copied in. The first `start` record in leaves.jsonl is from the aborted start.
- The leaves are cake_lpr-checked; the cover still has to be re-checked with `lake exe cover_check` (H3)
  once all four shards are in.
