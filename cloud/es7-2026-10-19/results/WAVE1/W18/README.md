# WAVE1 / W18: U10_L, shard 1 of 2 — CLOSED

Entry in `verify/ii_wave1.json`: `{"kind":"shard","case":"U10_L","shard":1,"nshards":2,"est_core_h":12.8}`.

## Where it ran
Cloud container, 4 cores, 15 GB RAM (`env.txt`), 2026-10-20 06:57–08:11 UTC. The solve itself ran 07:30–08:11.
Tools (`tools.txt`, binary hashes there): CaDiCaL c6073042 (3.0.1), march_cu CnC 705b60c6 (`-fcommon`),
cake_lpr a36874a8 (the bundled example gives `s VERIFIED UNSAT`). drat-trim / lrat-check was not used.

## sha256 checks (all match; `sha256_checks.txt`)
- `m33k7int.sub.cnf`, regenerated with the make_cnfs.sh steps (gen_etv.py 33 7 7 7 --mirror; mirgen.py --interior --yflip-unit):
  `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`
- `verify/ii_wave1.json`: `6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e`
- `results/Mii-S/cases.jsonl`: `bf77e23c6d9cdffb451a3ae63bdb972b4cc9589fbdca424e9cf0621f9e826f58`
- `U10_L.cnf` (`hullsplit.py case BASE 10 ""`): `7f6b84cd24133ecd7eb5f982ccff9d9012ae326d85263b7edf0898e668a02f3a`
- `U10_L/top.icnf` (`march_cu U10_L.cnf -d 7 -o top.icnf`, 250 s; log in `top_march.log`): 128 cubes, 0 refuted leaves,
  `9f1b517bec7eb6de62f1fa04c90a29ce9da95bb0de833c401fc0bdb1203a06e3`. W17 (shard 0) has the same hash.

## Method
`scripts/close_march.py` is `results/Mii-S/scripts/close_march.py` (kept unchanged as `scripts/close_march_orig.py`) with these additions:
- `--top`: a precomputed top-cube file;
- `--shard/--nshards`: only the cubes with 0-based line index i, i mod k == s;
- resume by replaying `leaves.jsonl`;
- solver files and the live log go to `--tmp` and `--state`, both outside the repo;
- a split record stores its children;
- `leaves.icnf` lists only leaves with `s VERIFIED UNSAT`;
- child CPU time is recorded;
- errors are logged.

Settings: `cadical --lrat -t 300`, splits by `march_cu -d 6`, 4 jobs. Only cake_lpr `s VERIFIED UNSAT` closes a leaf.

Run: `close_march.py U10_L.cnf U10_L --top top.icnf --shard 1 --nshards 2 --tmp … --state … --jobs 4`.

A first launch at 07:03 lost its records, so it was killed and restarted from scratch at 07:30. The cause: the
first commit put `leaves.jsonl` under git, and `git pull --rebase --autostash` then replaced that file while
the solver still had it open, so later records went to an unlinked file. The live log now lives outside the
repo and is copied in at each commit. None of those lost records is used.

## Result
- Shard 1 is the 64 top cubes with odd 0-based index.
- 59 top cubes were refuted directly. 3 timed out at 300 s and were split (`-d 6`: 64, 64, and 60 cubes of which 4 refuted).
  2 depth-13 children timed out again and were split (64, and 62 cubes of which 2 refuted).
- 373 leaves, all `UNSAT` with cake_lpr `s VERIFIED UNSAT`:
  - by depth: 61 at 7, 4 at 12, 182 at 13, 2 at 18, 124 at 19;
  - 5 split records; no SAT; no errors; `open.icnf` is empty.
- Every leaf extends a shard-1 top cube.
- `leaves.icnf` sha256: `9dd39e596f1b82f514ef7f407ca45fd704e09c9f94d1dac1535a5f632881287b`.
- Cover (`U10_L/covercheck.txt`):
  - `top.icnf` is COVERED (128);
  - `leaves.icnf` + the shard-0 top cubes is COVERED (437), so the leaves cover this shard's part;
  - W17's `leaves.icnf` + this `leaves.icnf` is COVERED (437), so **U10_L is closed as a whole**.
- CPU:
  - cadical 6309 s (max 296 s per run);
  - cake_lpr 1032 s (max 17.1 s);
  - split marches 1274 s;
  - top march 250 s;
  - largest proof 146 MB.

  Total about 2.5 core-h, against the 12.8 core-h estimate. The lost first launch used about 0.6 core-h more.

  Wall time for the solve: 41 min.
- No SAT.
