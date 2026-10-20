# WAVE1 / W17: U10_L, shard 0 of 2 — CLOSED

Entry in `verify/ii_wave1.json`: `{"kind":"shard","case":"U10_L","shard":0,"nshards":2,"est_core_h":12.8}`.

## Where it ran
Cloud container, 4 cores, 15 GB RAM (`env.txt`), 2026-10-20 06:56–07:30 UTC.
Tools (`tools.txt`): CaDiCaL c6073042 (3.0.1), march_cu CnC 705b60c6 (`-fcommon`),
cake_lpr a36874a8 (bundled example: `s VERIFIED UNSAT`). No drat-trim / lrat-check was used.

## sha256 checks (all match)
- `m33k7int.sub.cnf` regenerated (gen_etv.py 33 7 7 7 --mirror; mirgen.py --interior --yflip-unit):
  `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`
- `verify/ii_wave1.json`: `6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e`
- `U10_L.cnf` (`hullsplit.py case BASE 10 ""`): `7f6b84cd24133ecd7eb5f982ccff9d9012ae326d85263b7edf0898e668a02f3a`
- `U10_L.s0of2/top.icnf` (`march_cu U10_L.cnf -d 7`, 261.8 s): 128 cubes, 0 refuted leaves,
  `9f1b517bec7eb6de62f1fa04c90a29ce9da95bb0de833c401fc0bdb1203a06e3`. The shard-1 machine must get the same file.

## Method
`scripts/close_march.py` = `results/Mii-S/scripts/close_march.py` plus `--shard/--nshards`, a precomputed
`--top` file, a scratch dir for CNF/LRAT outside the repo, resume from `leaves.jsonl`, and
`leaves.icnf` / `open.icnf` written periodically. Settings: cadical `--lrat -t 300`, split `march_cu -d 6`,
4 jobs. Only `s VERIFIED UNSAT` from cake_lpr closes a leaf.
Run: `close_march.py U10_L.cnf U10_L.s0of2 --top top.icnf --shard 0 --nshards 2 --jobs 4`.
(`leaves.jsonl` has two `start` records: the first launch was killed with its shell before any cube finished.)

## Result
- Shard 0 = the 64 top cubes with 0-based index i, i mod 2 == 0.
- All 64 were refuted directly by CaDiCaL (no timeouts, no splits); all 64 proofs are `s VERIFIED UNSAT` under cake_lpr
  (no heap retries). `leaves.icnf` = 64 cubes = exactly the shard-0 top cubes; `open.icnf` is empty.
- Cover (`covercheck.txt`): `top.icnf` is COVERED (128); `leaves.icnf` + the shard-1 top cubes is COVERED,
  so the leaves cover this shard's part of U10_L.
- CPU: cadical 1469 s (max 105 s per cube), cake_lpr 341 s (max 18.6 s), largest proof 93 MB, plus 262 s for the top march.
  About 0.6 core-h in total, against an estimate of 12.8 core-h. Wall time about 8 min.
- No SAT.

U10_L as a whole is closed once shard 1 (cubes with odd index) is closed with the same top.icnf.
